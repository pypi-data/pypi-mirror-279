import inspect
import typing
from uuid import uuid4

from bstk_notitia.lib.abc.driver import DriverABC
from bstk_notitia.error import (
    NotitiaInvalidDriverParameter,
    NotitiaUnsupportedDriverCall,
)


class NotitiaModule(DriverABC):
    name = "Passthrough driver"
    key = "driver/passthrough"
    connections: typing.Dict[str, typing.Any]

    #
    # The passthrough driver provides a consistent interface for custom drivers.
    # You can use it as a simple registry to provide functionality to your modules without
    # having to create a full blown driver.
    #
    # The "dsn" provided to connect will be the object the driver will use, we generate
    # and return a "reference", which can be used to later disconnect or make calls.
    # You can make a "call" by providing the connection reference along with the method / params to execute.
    # Because we don't have a proper dsn, calling connect multiple times with the same
    # client will generate multiple references - so don't do that.
    #
    # Note that passthrough / custom drivers are not licenses to do random things in random ways.
    # Notitia modules exist to provide consistent and predictable behaviour, i.e. don't do weird shit.
    #
    def connect(self, dsn: typing.Any) -> typing.Any:
        if not dsn or not hasattr(dsn, "__class__"):
            raise NotitiaInvalidDriverParameter("Invalid DSN")

        _ref = self._genref()
        self.connections[_ref] = dsn

        return _ref

    # Remember - the dsn here is the reference returned by .connect
    def disconnect(self, dsn: str):
        if not dsn:
            return

        if dsn not in self.connections:
            return

        del self.connections[dsn]
        return

    def _genref(self) -> str:
        return str(uuid4())

    async def call(
        self, dsn: str, method: str, *args, **kwargs
    ) -> typing.Optional[typing.Dict]:
        if not dsn or dsn not in self.connections:
            raise NotitiaInvalidDriverParameter("Invalid DSN")

        _conn = self.connections[dsn]
        _call = getattr(_conn, method, None)
        if (
            _call is None
            or not callable(_call)
            or not inspect.iscoroutinefunction(_call)
        ):
            raise NotitiaUnsupportedDriverCall(
                f"{method} not suitable to be called on {_conn} (not defined, not callable, or not coro)"
            )

        return await _call(*args, **kwargs)
