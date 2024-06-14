from __future__ import annotations
from dataclasses import dataclass, field
import typing

import bson
from bstk_notitia.lib.abc.observer import ObserverABC
from datetime import datetime, UTC

if typing.TYPE_CHECKING:
    from modules.driver.mongodb import NotitiaModule as MongoDBDriver, DriverABC

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "mongodb",
        "required": True,
    }
}

# Establish and monitor a changestream, starting "now", and yield matching events as they arrive.
# The resume token is maintained within the observer
#
# When using this observer from an investigator, ensure you carefully consider the implications on the shift runner.
# A quiet collection that does not receive updates very often can cause the entire shift to run into overtime.
# Split your investigators into long lived pools until we get to py3.12
# ( https://docs.python.org/3.12/library/asyncio-task.html#waiting-primitives )


@dataclass
class NotitiaModule(ObserverABC):
    name = "Internal MongoDB Changestream"
    key = "internal/mongodb_changestream"
    resume_token: typing.AnyStr = field(init=False, default=None)

    if typing.TYPE_CHECKING:
        driver: typing.Dict[str, typing.Union[MongoDBDriver, DriverABC]]

    async def glance(self, document: typing.Dict) -> typing.Union[None, typing.Dict]:
        return document.get("fullDocument", None)

    async def monitor(
        self,
        collection: typing.AnyStr,
        lookup: typing.Optional[typing.Dict] = None,
        options: typing.Optional[typing.Dict] = None,
    ) -> typing.AsyncGenerator[bson.RawBSONDocument, None]:
        _pipeline = []
        if lookup:
            _pipeline.append(lookup)

        _collection = self.driver["mongodb"].get_collection(collection)
        if not self.resume_token and options and "resume_token" not in options:
            _cursor_start_time = self.driver["mongodb"].timestamp(datetime.now(UTC))
            options["start_at_operation_time"] = _cursor_start_time

        change_stream = self.driver["mongodb"].change_stream(
            collection=_collection,
            pipeline=_pipeline,
            **options,
        )
        async for token, change in self.driver["mongodb"].watch(change_stream):
            self.resume_token = token
            if not change:
                return

            doc = await self.glance(change[1])
            if not doc:
                continue

            yield doc
