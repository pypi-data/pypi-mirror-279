from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
import typing


if typing.TYPE_CHECKING:
    from bstk_notitia.lib.abc.driver import DriverABC
    from bstk_notitia.lib.abc.observer import ObserverABC
    from bstk_notitia.lib.abc.informant import InformantABC
    from bstk_notitia.lib.abc.reporter import ReporterABC


"""
Investigators specialise in working with a singular input,
collecting more information if required, deciding what to do
with that information, and then acting on that decision.

A good investigator has a narrow focus and works to quickly
close their case. They are a specialist at one particular task
and should not take more than a few seconds to come to a
conclusion (I/O not withstanding)

Complicated investigations lead to mistakes, so its usually
a good idea to have multiple investigators who specialise in
working with a discrete set of information and either create
new cases for other investigators, or reporting on their
case and closing it.

Abstracts aside, investigators:
  - hold the business logic
  - configure observers, informants and reporters
  - never change information directly
  - ensure each case is isolated from others
"""

NOTITIA_DEPENDENCIES: typing.Dict


@dataclass
class InvestigatorABC(ABC):
    department: typing.AnyStr = field(kw_only=True, default=None)
    name: typing.AnyStr = field(init=False)
    key: typing.AnyStr = field(init=False)
    type: typing.AnyStr = field(init=False, default="investigator")

    driver: typing.Dict[typing.AnyStr, DriverABC] = field(
        init=True, kw_only=True, default=None
    )
    observer: typing.Dict[typing.AnyStr, ObserverABC] = field(init=False, default=None)
    informant: typing.Dict[typing.AnyStr, InformantABC] = field(
        init=False, default=None
    )
    reporter: typing.Dict[typing.AnyStr, ReporterABC] = field(init=False, default=None)

    def sign_on(
        self,
        driver: typing.Optional[typing.Dict[typing.AnyStr, DriverABC]] = None,
        observer: typing.Optional[typing.Dict[typing.AnyStr, ObserverABC]] = None,
        informant: typing.Optional[typing.Dict[typing.AnyStr, InformantABC]] = None,
        reporter: typing.Optional[typing.Dict[typing.AnyStr, ReporterABC]] = None,
    ) -> typing.Dict:
        if driver:
            self.driver = driver
        if observer:
            self.observer = observer
        if informant:
            self.informant = informant
        if reporter:
            self.reporter = reporter

    @abstractmethod
    async def start(self, **kwargs):
        """
        'start' working... that could mean waiting for information from
        an observer, immediately reaching out to an informant, directly
        providing information to a report, or reach for a snack and wait..

        Investigators do whatever they do - we don't ask, they don't tell.
        """
        pass

    async def _stamp(
        self,
        document: typing.Dict,
        reporter: ReporterABC,
        updates: typing.Optional[typing.Dict] = None,
        constraints: typing.Optional[typing.Dict] = None,
    ):
        return await reporter.receive(
            action="update",
            record=document,
            data=updates,
            constraints=constraints,
        )

    async def mark(
        self,
        document: typing.Dict,
        reporter: ReporterABC,
        new_state: str,
    ):

        _log = (
            f"{self.key} #{document['number']} ({document['category']}) state change "
        )
        _log += f"{document['state']} -> {new_state}"

        constraints = {
            "state": {"$eq": document["state"]},
            "assigned_investigator": {"$in": [None, self.key]},
        }

        updates = {
            "state": new_state,
            "assigned_investigator": self.key,
        }
        if self.informant and "internal/datetime" in self.informant:
            updates["date"] = await self.informant["internal/datetime"].enquire()
        else:
            updates["date"] = datetime.now(tz=timezone.utc)

        _log += f" @ {updates['date'].isoformat()}"

        _stat = await self._stamp(
            document=document,
            reporter=reporter,
            updates=updates,
            constraints=constraints,
        )
        if _stat:
            document["state"] = new_state

        await self._log(_log, _stat)
        return _stat

    async def close(
        self,
        document: typing.Dict,
        reporter: ReporterABC,
        updates: typing.Optional[typing.Dict],
    ):
        return await self.record(
            document=document,
            reporter=reporter,
            updates=updates,
            new_state="complete",
        )

    async def record(
        self,
        document: typing.Dict,
        reporter: ReporterABC,
        updates: typing.Dict,
        new_state: typing.Optional[str] = None,
    ):
        _log = f"{self.key} #{document['number']} ({document['category']}) case update [{updates}] "
        _log += f"{document['state']} -> {new_state}"

        constraints = {
            "state": {"$eq": document["state"]},
            "assigned_investigator": {"$eq": self.key},
        }

        if new_state:
            updates["state"] = new_state
        if "internal/datetime" in self.informant:
            updates["date"] = await self.informant["internal/datetime"].enquire()
        else:
            updates["date"] = datetime.now(tz="UTC")

        _log += f" @ {updates['date'].isoformat()}"

        _stat = await self._stamp(
            document=document,
            reporter=reporter,
            updates=updates,
            constraints=constraints,
        )
        if _stat and new_state:
            document["state"] = new_state

        await self._log(_log, _stat)
        return _stat

    async def _log(self, message, stat):
        print(("✔︎ " if stat else "✕ ") + message)
