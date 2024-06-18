from __future__ import annotations
from dataclasses import dataclass, field
import typing
from datetime import datetime, UTC

from bstk_notitia.lib.abc.observer import ObserverABC

if typing.TYPE_CHECKING:
    from bstk_notitia.modules.driver.mongodb import (
        NotitiaModule as MongoDBDriver,
        DriverABC,
    )

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "mongodb",
        "required": True,
    },
}

# Where the mongo record observer does a "find all", and the mongo change stream observer "watches" for
# changes, the notitia collection stream observer wraps both up into a consolidated "find & watch" observer,
# whereby it will establish a change stream starting "now", find all pre-existing items matching the lookup,
# yield until empty, then move on to results from the change stream.
#
# When using this observer from an investigator, ensure you carefully consider the implications on the shift runner.
# A quiet collection that does not receive updates very often can cause the entire shift to run into overtime.
# Split your investigators into long lived pools until we get to py3.12
# ( https://docs.python.org/3.12/library/asyncio-task.html#waiting-primitives )


@dataclass
class NotitiaModule(ObserverABC):
    name = "Internal Mongo Collection Observer"
    key = "internal/mongo_collectionstream"

    if typing.TYPE_CHECKING:
        driver: typing.Dict[str, typing.Union[MongoDBDriver, DriverABC]]

    collection: typing.AnyStr = field(kw_only=True, default=None)

    lookup: typing.Optional[typing.Union[typing.List[typing.Dict], typing.Dict]] = (
        field(kw_only=True, default=None)
    )
    operations: typing.Optional[typing.List[typing.AnyStr]] = field(
        kw_only=True, default_factory=list
    )

    def __post_init__(self):
        if not self.operations:
            self.operations = ["insert", "update", "replace"]

    async def glance(self, document: typing.Dict) -> typing.Union[None, typing.Dict]:
        return document.get("fullDocument", None)

    async def monitor(
        self,
        lookup: typing.Optional[
            typing.Union[typing.List[typing.Dict], typing.Dict]
        ] = None,
    ) -> typing.AsyncGenerator[typing.Dict, None]:
        if not self.operations:
            return

        if self.lookup:
            if not lookup:
                lookup = self.lookup
            else:
                lookup = {**lookup, **self.lookup}

        _lookup = {"$match": {"operationType": {"$in": self.operations}}}
        if lookup:
            for _k, _v in lookup.items():
                _lookup["$match"][f"fullDocument.{_k}"] = _v

        prematch_hits = []

        _cursor_start_time = self.driver["mongodb"].timestamp(datetime.now(UTC))
        _collection = self.driver["mongodb"].get_collection(self.collection)
        async for doc in _collection.find(lookup):
            prematch_hits.append(doc["_id"])
            yield doc

        _stream_params = {
            "collection": _collection,
            "pipeline": [_lookup],
            "resume_token": None,
            "full_document": "updateLookup",
        }
        change_stream = self.driver["mongodb"].change_stream(
            **_stream_params,
            start_at_operation_time=_cursor_start_time,
        )

        async for token, change in self.driver["mongodb"].watch(
            changestream=change_stream, **_stream_params
        ):
            if not change:
                # Something's gone wrong, stop.
                break

            _stream_params["resume_token"] = token
            _t = change.get("operationType")
            if _t not in self.operations:
                # We should never see this, so if we do - it's a sign things have gone poorly
                break

            doc = await self.glance(change)
            if not doc:
                continue

            if doc["_id"] in prematch_hits:
                prematch_hits.remove(doc["_id"])
                continue

            yield doc
