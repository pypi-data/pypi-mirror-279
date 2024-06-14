import copy
from dataclasses import dataclass, field
import decimal
import typing


from bstk_notitia.lib.abc.driver import DriverABC

import bson
from bson import codec_options, Timestamp
import motor.motor_asyncio
import motor.docstrings
import pymongo.errors

from datetime import datetime, date, time, UTC
from enum import Enum


def _bson_encode(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, decimal.Decimal):
        return bson.Decimal128(value)
    if (
        isinstance(value, object)
        and hasattr(value, "_to_json")
        and callable(value._to_json)
    ):
        return value._to_json()

    if isinstance(value, date):
        return datetime.combine(value, time.min)

    return None


class DecimalCodec(codec_options.TypeCodec):
    python_type = decimal.Decimal  # the Python type acted upon by this type codec
    bson_type = bson.Decimal128  # the BSON type acted upon by this type codec

    def transform_python(self, value: decimal.Decimal):
        """Function that transforms a custom type value into a type
        that BSON can encode. We use a precision of 30 to avoid overflows
        and other weird shit that happens during floatfuckery"""
        return bson.Decimal128(decimal.Context(prec=30).create_decimal(value))

    def transform_bson(self, value: bson.Decimal128):
        """Function that transforms a vanilla BSON type value into our
        custom type."""
        return value.to_decimal()


mongod_params = {
    "connectTimeoutMS": "2000",
    "heartbeatFrequencyMS": "1000",
    "serverSelectionTimeoutMS": "5000",
    "tz_aware": True,
    "uuidRepresentation": "pythonLegacy",
    "type_registry": codec_options.TypeRegistry(
        [DecimalCodec()], fallback_encoder=_bson_encode
    ),
}


@dataclass
class NotitiaModule(DriverABC):
    """
    The mongodb driver module provides a thin facade around mongo_motor.

    In general, all modules can use different collections and databases,
    but the DSN is managed per-department.

    Implementors can be specific, targeting databases and collections,
    or implicit, using the parameters provided by the investigator during
    startup.

    Regardless of which implementation is used, the only interface provided
    by this module that wouldn't normally be available is the `watch` command
    which provides a functional wrapper around a mongo change stream.
    """

    name = "MongoDB (Motor) driver"
    key = "driver/mongodb"

    dsn: typing.Optional[typing.AnyStr] = field(kw_only=True, default=None)
    params: typing.Optional[typing.Dict] = field(kw_only=True, default_factory=dict)
    database: typing.Optional[typing.AnyStr] = field(kw_only=True, default=None)
    collection: typing.Optional[typing.AnyStr] = field(kw_only=True, default=None)
    connections: typing.Dict[typing.AnyStr, motor.motor_asyncio.AsyncIOMotorClient] = (
        field(init=False, default_factory=dict)
    )

    def __post_init__(self):
        if True:
            # Fixed in 4.8 [https://jira.mongodb.org/browse/PYTHON-4449]
            def _change_stream_options(self) -> dict[str, typing.Any]:
                """Return the options dict for the $changeStream pipeline stage."""
                options: dict[str, typing.Any] = {}
                if self._full_document is not None:
                    options["fullDocument"] = self._full_document

                if self._full_document_before_change is not None:
                    options["fullDocumentBeforeChange"] = (
                        self._full_document_before_change
                    )

                resume_token = self.resume_token
                if resume_token is not None:
                    if self._uses_start_after:
                        options["startAfter"] = resume_token
                    else:
                        options["resumeAfter"] = resume_token

                elif self._start_at_operation_time is not None:
                    options["startAtOperationTime"] = self._start_at_operation_time

                if self._show_expanded_events:
                    options["showExpandedEvents"] = self._show_expanded_events

                return options

            from pymongo.change_stream import ChangeStream

            ChangeStream._change_stream_options = _change_stream_options

    # Notitia
    def connect(
        self, dsn: typing.Optional[typing.AnyStr] = None
    ) -> motor.motor_asyncio.AsyncIOMotorClient:
        if not dsn and self.dsn:
            dsn = self.dsn

        if dsn not in self.connections:
            _params = {**mongod_params, **self.params}
            self.connections[dsn] = motor.motor_asyncio.AsyncIOMotorClient(
                dsn, **_params
            )

        return self.connections[dsn]

    def disconnect(self, dsn: typing.Optional[str] = None):
        if dsn:
            if dsn not in self.connections:
                return

            self.connections[dsn].close()
            return

        for _conn in self.connections.values():
            _conn.close()

    # Native
    def get_db(
        self,
        name: typing.Optional[str] = None,
        client: typing.Optional[motor.motor_asyncio.AsyncIOMotorClient] = None,
    ) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        if client is None and self.dsn:
            client = self.connect(self.dsn)

        if not name and self.database:
            name = self.database

        return client[name]

    def get_collection(
        self,
        name: typing.Optional[str] = None,
        db: typing.Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None,
    ) -> motor.motor_asyncio.AsyncIOMotorCollection:
        if db is None and self.dsn and self.database:
            db = self.get_db()

        if not name and self.collection:
            name = self.collection

        return db[name]

    def timestamp(self, date: typing.Optional[datetime] = None) -> Timestamp:
        if not date:
            date = datetime.now(UTC)
        return Timestamp(time=date, inc=0)

    def change_stream(
        self,
        pipeline: typing.List,
        collection: typing.Optional[motor.motor_asyncio.AsyncIOMotorCollection] = None,
        resume_token: typing.Optional[typing.AnyStr] = None,
        start_token: typing.Optional[typing.AnyStr] = None,
        **kwargs,
    ) -> motor.motor_asyncio.AsyncIOMotorChangeStream:
        if collection is None:
            if not self.collection:
                raise ValueError("Cannot auto-select collection")
            collection = self.get_collection(self.collection)

        params = {**kwargs}

        if not params:
            params = {}
        params["pipeline"] = pipeline
        if resume_token:
            params["resume_after"] = resume_token
        if start_token:
            params["start_after"] = start_token

        return collection.watch(**params)

    async def watch(
        self,
        pipeline: typing.Optional[typing.List[typing.Dict]] = None,
        collection: typing.Optional[motor.motor_asyncio.AsyncIOMotorCollection] = None,
        resume_token: typing.Optional[typing.AnyStr] = None,
        start_token: typing.Optional[typing.AnyStr] = None,
        changestream: typing.Optional[
            motor.motor_asyncio.AsyncIOMotorChangeStream
        ] = None,
        **kwargs,
    ) -> typing.AsyncGenerator[typing.Tuple[typing.AnyStr, typing.Dict], None]:

        if not changestream:
            if not pipeline:
                raise ValueError(
                    "If changestream is not provided, you must provide something for the pipeline"
                )

            changestream = self.change_stream(
                pipeline=pipeline,
                collection=collection,
                resume_token=resume_token,
                start_token=start_token,
                **kwargs,
            )

        try:
            async with changestream as stream:
                async for change in stream:
                    resume_token = stream.resume_token
                    yield (resume_token, change)

        except pymongo.errors.OperationFailure as ex:

            # If we tripped over an "invalidate", a 260 will be thrown.
            # If there's a resume token within the changstream, use it as a start token
            # and go around one last time
            if ex.code == 260 and changestream.resume_token:
                start_token = copy.deepcopy(changestream.resume_token)
                resume_token = None
            elif resume_token is None:
                raise

            changestream = self.change_stream(
                pipeline=pipeline,
                collection=collection,
                resume_token=resume_token,
                start_token=start_token,
                **kwargs,
            )

            async with changestream as stream:
                async for change in stream:
                    resume_token = stream.resume_token
                    yield (resume_token, change)
