from __future__ import annotations
import asyncio
from dataclasses import dataclass, field
import sys
import traceback
import typing
from bstk_notitia.lib.abc.investigator import InvestigatorABC

if typing.TYPE_CHECKING:
    import datetime
    from modules.driver.mongodb import NotitiaModule as MongoDBDriver, DriverABC

"""
This sample investigator is a mongodb record "enricher".

It asks the observer to collect records from a
particular collection that have not been collected,
gets the current date from the date reporter
and tells the mongo_record reporter that it
has changes to report.

Being a busywork investigator, it always tells
the reporter that it has a new record to report
before the observer is even engaged - so its
always got _something_ to do.
"""

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "mongodb",
        "required": True,
        "params": {
            "dsn": "mongodb://localhost",
        },
    },
    "observer": {
        "type": "internal/mongo_collectionstream",
        "required": True,
        "params": {
            "lookup": {"reported": {"$ne": True}},
        },
    },
    "informant": {
        "type": "internal/datetime",
        "required": True,
    },
    "reporter": [
        {
            "type": "internal/mongo_record",
            "required": True,
        },
        {
            "type": "internal/echo",
            "required": True,
        },
    ],
}


@dataclass
class NotitiaModule(InvestigatorABC):
    name = "Internal Notitia Case Reporter"
    key = "internal/notitia_casereporter"
    driver: typing.Dict[str, typing.Union[MongoDBDriver, DriverABC]]

    case_limit: typing.SupportsInt = field(init=False, default=None)

    def sign_on(
        self,
        case_limit: typing.Optional[typing.SupportsInt] = None,
        *args,
        **kwargs,
    ):
        self.case_limit = case_limit
        super().sign_on(*args, **kwargs)

    async def start(self, **kwargs):
        if not self.case_limit:
            self.case_limit = 10

        try:
            case_counter = 0
            while self.case_limit == 0 or case_counter < self.case_limit:
                print("tick..")
                async for document in self.observer[
                    "internal/mongo_collectionstream"
                ].monitor():
                    case_counter += 1
                    data: datetime.datetime = await self.informant[
                        "internal/datetime"
                    ].enquire()

                    res = await self.reporter["internal/mongo_record"].receive(
                        action="update",
                        record=document,
                        data={"reported": True, "reported_at": data},
                    )
                    await self.reporter["internal/echo"].receive(
                        {
                            f"Reporting on case {case_counter} of {self.case_limit} @ {data.isoformat()}": document,
                            "Result": res,
                        }
                    )
                    if self.case_limit and case_counter >= self.case_limit:
                        break

                await asyncio.sleep(1)

        except Exception:
            traceback.print_exc(file=sys.stdout, chain=True)
            raise

        return
