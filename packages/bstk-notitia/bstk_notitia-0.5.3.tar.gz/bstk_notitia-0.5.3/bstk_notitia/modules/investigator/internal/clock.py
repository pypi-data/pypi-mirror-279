from dataclasses import dataclass, field
import datetime
import typing
from bstk_notitia.lib.abc.investigator import InvestigatorABC

"""
This sample investigator is a clock watcher.

It doesn't do anything interesting, but it does it reliably
from the moment it clocks on, until it clocks off.
"""

NOTITIA_DEPENDENCIES = {
    "driver": [
        {
            "type": "null",
            "required": True,
        },
        {
            "type": "null",
            "required": True,
        },
    ],
    "observer": {
        "type": "internal/tick",
        "required": True,
        "params": {"interval": "2"},
    },
    "informant": {
        "type": "internal/datetime",
        "required": True,
    },
    "reporter": {
        "type": "internal/echo",
        "required": True,
    },
}


@dataclass
class NotitiaModule(InvestigatorABC):
    name = "Internal Clock Investigator"
    key = "internal/clock"

    target_timezone: typing.List[typing.AnyStr] = field(
        kw_only=True, default_factory=list
    )

    async def start(self, **kwargs):
        if not self.observer or not self.informant or not self.reporter:
            return

        async for _ in self.observer["internal/tick"].monitor():
            data: datetime.datetime = await self.informant[
                "internal/datetime"
            ].enquire()
            await self.reporter["internal/echo"].receive(
                {"The date is": data.isoformat()}
            )
