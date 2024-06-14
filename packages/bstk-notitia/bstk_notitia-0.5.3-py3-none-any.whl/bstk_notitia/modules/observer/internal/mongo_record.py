from __future__ import annotations
from dataclasses import dataclass, field
import typing

from bstk_notitia.lib.abc.observer import ObserverABC

if typing.TYPE_CHECKING:
    from modules.driver.mongodb import NotitiaModule as MongoDBDriver, DriverABC

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "mongodb",
        "required": True,
    }
}


@dataclass
class NotitiaModule(ObserverABC):
    name = "Internal MongoDB Record"
    key = "internal/mongo_record"

    if typing.TYPE_CHECKING:
        driver: typing.Dict[str, typing.Union[MongoDBDriver, DriverABC]]

    collection: typing.AnyStr = field(kw_only=True, default=None)
    lookup: typing.Optional[typing.Union[typing.List[typing.Dict], typing.Dict]] = (
        field(kw_only=True, default=None)
    )

    async def glance(self, document: typing.Dict) -> typing.Union[None, typing.Dict]:
        pass

    async def monitor(
        self,
        options: typing.Optional[typing.Dict] = None,
        lookup: typing.Optional[
            typing.Union[typing.List[typing.Dict], typing.Dict]
        ] = None,
    ) -> typing.AsyncGenerator[typing.Dict, None]:
        if self.lookup:
            if not lookup:
                lookup = self.lookup
            else:
                lookup = {**lookup, **self.lookup}

        async for _doc in (
            self.driver["mongodb"].get_collection(self.collection).find(lookup)
        ):
            yield _doc
