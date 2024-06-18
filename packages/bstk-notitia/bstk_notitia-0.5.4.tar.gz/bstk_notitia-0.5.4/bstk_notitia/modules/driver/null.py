import typing

from bstk_notitia.lib.abc.driver import DriverABC


class NotitiaModule(DriverABC):
    name = "Null driver"
    key = "driver/null"
    connections: typing.Dict[str, None]

    # Notitia
    def connect(self, dsn: str) -> None:
        if dsn not in self.connections:
            self.connections[dsn] = None

        return self.connections[dsn]

    def disconnect(self, dsn: typing.Optional[str] = None):
        if dsn:
            if dsn not in self.connections:
                return

            del self.connections[dsn]
            return
