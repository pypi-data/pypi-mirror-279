from dataclasses import dataclass, field
import typing
from bstk_notitia.lib.abc.observer import ObserverABC
from timedelta_isoformat import timedelta
from datetime import datetime
from asyncio import sleep

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "null",
        "required": True,
    },
}


@dataclass
class NotitiaModule(ObserverABC):
    name = "Internal Tick Observer"
    key = "internal/tick"
    interval: typing.SupportsFloat = field(kw_only=True, default=2)

    async def glance(self, target: typing.AnyStr) -> bool:
        if not target:
            return False

        try:
            timedelta.fromisoformat(target)
        except Exception:
            return False

        return True

    async def monitor(
        self, target: typing.Optional[float] = None
    ) -> typing.Union[datetime, typing.AsyncGenerator[datetime, None]]:
        _is_persistent: bool = False
        if target:
            _is_persistent = True

        if not target and self.interval:
            target = self.interval

        target = f"PT{target}S"

        if not await self.glance(target):
            raise ValueError("Invalid tick target")

        delta = timedelta.fromisoformat(target)
        now = datetime.now()

        while 1:
            until = now + delta
            tosleep = (until - now).total_seconds()
            await sleep(tosleep)
            yield until
            if not _is_persistent:
                break
