from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
from enum import Enum
import typing
import queue
from uuid import uuid4

import concurrent.futures
import sys
import traceback


if typing.TYPE_CHECKING:
    from lib.abc.investigator import InvestigatorABC

"""
The roster is responsible for managing investigators and their
associated tasks.

When an investigator is added to the roster, it will:
 - Create a new threadpool for that investigator and its observers
 - Instantiate any observers required by the investigator
 - Connect a dispatcher to the investigators threadpool
 - Ensure investigators clean up after themselves

The roster limits the number of active investigators clocked on,
but can have an infinite pool of investigators waiting for a shift.

It also controls how many jobs can be executed in a shift, along with
how long an investigator can run for before it needs to take a break.

If an investigator is marked as "always on", the shift limit still
applies, but the investigator will be immediately reinstated as soon
as a slot becomes available, (always on investigators have a priority of
1, the rest as priority 10). Investigators that are not "always on"
form an orderly queue, based on when they were added to the roster,
(FIFO).

So long as an investigator is not in the middle of anything (ie:
waiting for an observer), it will be clocked off. Slow investigations
lead to slower shift cycles and limit the overall throughput

"""


class RosterType(Enum):
    PERMANENT = 1
    CASUAL = 2


class Roster:
    investigator_limit: int = 10
    shift_limit: int = 30
    _shift_pools: typing.Dict[str, queue.Queue] = None
    _active_shift: ShiftManager = None

    def __init__(
        self, limit: typing.Optional[int] = None, duration: typing.Optional[int] = None
    ) -> None:
        if limit:
            self.investigator_limit = limit
        if duration:
            self.set_duration(duration)

    def set_duration(self, duration: int) -> None:
        self.shift_limit = duration

    def _initialise_shift_pools(self):
        if self._shift_pools is not None:
            return

        self._shift_pools = {
            RosterType.PERMANENT.name: queue.Queue(),
            RosterType.CASUAL.name: queue.Queue(),
        }

    def add(
        self,
        investigator: InvestigatorABC,
        type: RosterType,
        startup_params: typing.Optional[typing.Dict] = None,
    ):
        if not self._shift_pools:
            self._initialise_shift_pools()

        if not isinstance(type, RosterType):
            raise ValueError("`type` must be a `RosterType`")

        self._shift_pools[type.name].put_nowait(investigator)

    def get_shift(self) -> ShiftManager:
        if not self._shift_pools:
            raise Exception("No shift pools available - add an investigator first")

        if self._active_shift is not None:
            raise Exception("Already an active shift running - end it first")

        self._active_shift = ShiftManager(
            limit=self.investigator_limit,
            duration=self.shift_limit,
        )

        self._active_shift.populate_pools(self._shift_pools)

        return self._active_shift

    async def end_shift(self) -> None:
        if self._active_shift is None:
            return

        await self._active_shift.end()


class ShiftManager:
    """
    The shift manager sets up investigations, ready for the shift
    coordinator to distribute to workstations.

    Investigations that are "permanent" have a higher priority than
    casual investigations.

    The default cycle rate is set to `2` (a cycle ever two seconds).

    Once pools are populated, `start()` will return a coro that
    can be thrown over to an executor and run
    """

    pools: typing.Dict[str, queue.Queue[Investigation]] = None
    _shift_coordinator: ShiftCoordinator = None

    def __init__(
        self,
        limit: typing.Optional[int] = 10,
        duration: typing.Optional[int] = 0,
    ):
        cycle_rate = 2
        cycle_limit = None
        if duration:
            cycle_limit = duration / cycle_rate

        self._shift_coordinator = ShiftCoordinator(
            limit, cycle_rate=cycle_rate, cycle_limit=cycle_limit
        )

    def populate_pools(self, pools: typing.Dict[str, queue.Queue]):
        while not pools[RosterType.PERMANENT.name].empty():
            self._shift_coordinator.add_investigation(
                Investigation(
                    priority=1,
                    id=str(uuid4()),
                    investigator=pools[RosterType.PERMANENT.name].get(),
                )
            )

        while not pools[RosterType.CASUAL.name].empty():
            self._shift_coordinator.add_investigation.append(
                Investigation(
                    priority=10,
                    id=str(uuid4()),
                    investigator=pools[RosterType.CASUAL.name].get(),
                )
            )

    """
    Changing the cycle rate and limit here imply you know what you
    are trying to do. Otherwise, just use `Roster.set_duration` to
    change how long a shift lasts for prior to getting the shift.
    """

    def start(
        self,
        cycle_rate: typing.Optional[float] = None,
        cycle_limit: typing.Optional[float] = None,
        workstation_isolation: typing.Optional[bool] = None,
    ) -> typing.Coroutine:
        return self._shift_coordinator.start(
            cycle_rate=cycle_rate,
            cycle_limit=cycle_limit,
            workstation_isolation=workstation_isolation,
        )

    def end(self) -> typing.Coroutine:
        return self._shift_coordinator.finish()


class ShiftCoordinator:
    """
    The shift coordinator creates a pool of workstations that
    can accept investigations. The workstations collect
    investigations from the shift pool based on their priority
    and will deposit them back onto the queue once each
    investigation is complete

    The shift coordinator ensures the requested number
    of workstations are available to be used for investigation
    along with how long the shift will go for.

    Calling `start()` will return a coroutine which can be
    executed in the appropriate context.
    """

    investigations: typing.List[Investigation] = None

    _started: bool = False
    _finishing: bool = False

    _tickrate: float
    _ticklimit: float

    shift_pool: queue.PriorityQueue[Investigation] = None
    workstations: typing.List[Workstation] = None
    workstation_isolation: bool

    max_workstation_count: int = 10
    occupied_workstations: set

    def __init__(
        self,
        limit: typing.Optional[int] = 10,
        investigations: typing.Optional[typing.List[Investigation]] = None,
        cycle_rate: typing.Optional[float] = 1,
        cycle_limit: typing.Optional[float] = 0,
        workstation_isolation: typing.Optional[bool] = False,
    ) -> None:
        self.investigations = []
        if investigations:
            for _investigation in investigations:
                self.add_investigation(_investigation)

        if limit < 1:
            raise ValueError("`limit` must be a non-zero integer")
        self.max_workstation_count = limit

        if cycle_rate:
            self._tickrate = cycle_rate

        if cycle_limit:
            self._ticklimit = cycle_limit

        self.workstation_isolation = workstation_isolation

        self.shift_pool = asyncio.PriorityQueue()
        self.occupied_workstations = set()

    @property
    def occupied_workstation_count(self) -> int:
        return len(self.occupied_workstations)

    def open_workstation(self, workstation: Workstation) -> None:
        open = workstation.open_for_investigation()
        self.occupied_workstations.add(open)
        asyncio.create_task(self._open_workstation(open))

    async def _open_workstation(self, coro: typing.Coroutine) -> None:
        try:
            return await coro
        except Exception:
            print("Exception when opening workstation..")
            print("-" * 60)
            traceback.print_exc(file=sys.stdout, chain=True)
            print("-" * 60)
        finally:
            self.occupied_workstations.remove(coro)

    def add_investigation(self, investigation: Investigation) -> None:
        self.investigations.append(investigation)

    def start(
        self,
        cycle_rate: typing.Optional[float] = None,
        cycle_limit: typing.Optional[float] = None,
        workstation_isolation: typing.Optional[bool] = None,
    ) -> typing.Coroutine:
        if self._started:
            raise RuntimeError("Already started")

        if len(self.investigations) < 1:
            raise RuntimeError("Nothing to do")

        if cycle_rate is not None:
            self._tickrate = cycle_rate

        if cycle_limit is not None:
            self._ticklimit = cycle_limit

        if workstation_isolation is not None:
            self.workstation_isolation = workstation_isolation

        self.max_workstation_count = min(
            self.max_workstation_count, len(self.investigations)
        )

        for _i in self.investigations:
            self.shift_pool.put_nowait(_i)

        self.workstations = [
            Workstation(
                id=_, queue=self.shift_pool, isolation=self.workstation_isolation
            )
            for _ in range(self.max_workstation_count)
        ]

        return self._start()

    async def _start(self) -> None:
        self._started = True
        _ticker = 0

        print(f"< [{self._ticklimit}] @ [{self._tickrate}] >")
        while self._finishing is not True:
            if _ticker > 0:
                await asyncio.sleep(self._tickrate)

            _ticker += 1
            if self._ticklimit and self._ticklimit < _ticker:
                await self.finish()
                print(f"< {_ticker} X {self._ticklimit} >")
                break

            # No point even trying if the pool is full
            if self.shift_pool.full():
                print(f"<!- {_ticker} -!>")
                continue

            idle_workstations = [_w for _w in self.workstations if _w.available is True]
            if not idle_workstations:
                print(f"<o {_ticker} o>")
                continue

            for idle_workstation in idle_workstations:
                if not idle_workstation:
                    print(f"<? {_ticker} ?>")
                    continue

                idle_workstation.available = False
                self.open_workstation(idle_workstation)
                print(f"< {_ticker} +{idle_workstation.id} >")

        while self.occupied_workstation_count > 0:
            await self.finish()
            await asyncio.sleep(0.3)

    async def finish(self):
        """
        Prevent workstations from being opened and signal
        all active workstations that they should finish
        """
        self._finishing = True
        for _w in self.workstations:
            if _w.available is False or _w.closing:
                continue
            await _w.close()


"""
An investigation is a prioritisation and identification
concept - it does very little other than ensure correct
queueing behaviour
"""


@dataclass(order=True)
class Investigation:
    priority: int
    id: int = field(compare=False)
    investigator: InvestigatorABC = field(compare=False)


"""
Workstations are where investigations are worked on by
investigators. They are semi-autonomous, pull items off
the shift pool when available and put them back afterwards.

Workstations are well behaved, in that they will reboot
themselves if no investigations become available within
`idle_limit` seconds - helping to speed up shift closure.

Workstations have limited patience and will not wait for
and investigator if they're taking too long. To allow
for other investigations that may have faster or more urgent
work, it will wait for an investigator no longer than
`session_limit` seconds to complete their work.

Each workstation maintains its own event loop, ensuring
that the workstation remains nice and clean between
investigations and that a heavy workload on one
workstation does impact other workstations. To facilitate
this cleanliness, thread pools are only stood up when
and investigation starts and torn down as soon as it finishes.
"""


class Workstation:
    id: int
    queue: asyncio.PriorityQueue[Investigation]
    available: bool
    closing: bool
    idle_limit: int
    session_limit: int
    isolate: bool

    def __init__(
        self,
        id: int,
        queue: asyncio.PriorityQueue[Investigation],
        idle_limit: typing.Optional[int] = 10,
        session_limit: typing.Optional[int] = None,
        isolation: typing.Optional[bool] = False,
    ):
        self.available = True
        self.closing = False
        self.id = id
        self.queue = queue
        self.idle_limit = idle_limit
        self.session_limit = session_limit
        self.isolation = isolation

    async def open_for_investigation(self):
        self.available = False
        try:
            async with asyncio.timeout(self.idle_limit):
                investigation = await self.queue.get()
        except TimeoutError:
            print(f"< -{self.id} >")
            self.available = True
            return

        print(
            f"Workstation #{self.id} occupied by"
            + f" [p{investigation.priority}]{investigation.id} /"
            + f" {investigation.investigator.key} {asyncio.current_task().get_name()}",
        )
        activity = None
        try:
            _coro = investigation.investigator.start()
            if self.isolation:
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=3, thread_name_prefix=f"nwk_{self.id}"
                ) as executor:
                    activity = executor.submit(asyncio.run, _coro)

                    activity.result(self.session_limit)

                    """
                    Need some way of ensuring the task goes away if we need it to....
                    ```
                    while not activity.done():
                        await asyncio.sleep(1)
                        if self.closing:
                            activity.cancel()
                            break
                    ```
                    """
            else:
                if self.session_limit:
                    _ = asyncio.wait_for(_coro, self.session_limit)
                else:
                    await _coro

            print(
                f"Workstation #{self.id} relinquished by"
                + f" [p{investigation.priority}]{investigation.id} /"
                + f" {investigation.investigator.key} {asyncio.current_task().get_name()}",
            )
        except TimeoutError:
            if activity:
                activity.cancel()
            print(
                f"Workstation #{self.id} gave after {self.session_limit}s"
                + f" [p{investigation.priority}]{investigation.id} /"
                + f" {investigation.investigator.key} {asyncio.current_task().get_name()}",
            )
        except Exception:
            print(
                f"Workstation #{self.id} caught an error in"
                + f" {investigation.id} / {investigation.investigator.key}"
            )
            traceback.print_exc(file=sys.stdout, chain=True)

        self.queue.task_done()
        await self.queue.put(investigation)
        print(f"< -{self.id} >")
        self.available = True

    async def close(self):
        print(f"Workstation #{self.id} being asked to close")
        self.closing = True
