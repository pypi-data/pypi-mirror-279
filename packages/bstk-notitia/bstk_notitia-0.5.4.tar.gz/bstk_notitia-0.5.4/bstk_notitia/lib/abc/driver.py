from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import typing

"""
A Notitia driver is a storage or streaming data source that can be used
across all other modules.

Unlike other modules, drivers are instanciated once and made available to
other modules that request it in their dependency spec.

Notitia holds and provides connection strings, authentication information,
etc, so modules purely need to know what dsn they should use.
"""


@dataclass
class DriverABC(ABC):
    department: typing.AnyStr = field(kw_only=True, default=None)
    name: typing.AnyStr = field(init=False)
    key: typing.AnyStr = field(init=False)
    type: typing.AnyStr = field(init=False, default="driver")

    connections: typing.Dict[typing.AnyStr, typing.Any] = field(
        init=False, default_factory=dict
    )

    def set_up(self, dsn: typing.Any) -> typing.Dict:
        self.connect(dsn)

    @abstractmethod
    def connect(self, dsn: typing.Any):
        """
        Connect to the specified DSN and return a "client like" reference that
        can be used to communicate with the service
        """
        pass

    @abstractmethod
    def disconnect(self, dsn: typing.Optional[typing.Any]):
        """
        If provided with a dsn and we have an active connection using it, disconnect
        from it.
        If no dsn is provided, disconnect from everything (shut down)
        """
        pass
