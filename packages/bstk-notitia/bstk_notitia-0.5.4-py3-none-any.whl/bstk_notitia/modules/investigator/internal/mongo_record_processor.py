from __future__ import annotations
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
        "type": "internal/mongo_record",
        "required": True,
        "params": {
            "lookup": {"collected": False},
        },
    },
    "informant": {
        "type": "internal/datetime",
        "required": True,
    },
    "reporter": {
        "type": "internal/mongo_record",
        "required": True,
    },
}


class NotitiaModule(InvestigatorABC):
    name = "Internal MongoDB Record Collector"
    key = "internal/mongo_record_processor"
    driver: typing.Dict[str, typing.Union[MongoDBDriver, DriverABC]]

    async def start(self, **kwargs):

        async for document in self.observer["internal/mongo_record"].monitor():
            data: datetime.datetime = await self.informant[
                "internal/datetime"
            ].enquire()
            res = await self.reporter["internal/mongo_record"].receive(
                action="update",
                record=document,
                data={"collected": True, "collected_at": data},
            )
            print(f"{res}")
