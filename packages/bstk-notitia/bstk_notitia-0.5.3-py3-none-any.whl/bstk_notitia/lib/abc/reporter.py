from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import typing

if typing.TYPE_CHECKING:
    from lib.abc.driver import DriverABC

"""
Reporters disseminate information provided to them by
investigators. The reporter understands how to publish to
a particular medium and formats the information to suit
its target audience.

Given the nature of data - reporters can be used to alter
the current state of information, (by writing to a source),
meaning they can make changes without necessarily making
information public.

Outside of invalid data or format limitations, reporters
cannot choose to withold information - they are impartial
intermediatries.
"""

NOTITIA_DEPENDENCIES: typing.Dict


@dataclass
class ReporterABC(ABC):
    department: typing.AnyStr = field(kw_only=True, default=None)
    name: typing.AnyStr = field(init=False)
    key: typing.AnyStr = field(init=False)
    type: typing.AnyStr = field(init=False, default="reporter")

    driver: typing.Dict[typing.AnyStr, DriverABC] = field(
        init=True, kw_only=True, default=None
    )

    def sign_on(self) -> typing.Dict:
        pass

    @abstractmethod
    async def receive(self, **kwargs):
        pass

    @abstractmethod
    async def publish(self):
        pass
