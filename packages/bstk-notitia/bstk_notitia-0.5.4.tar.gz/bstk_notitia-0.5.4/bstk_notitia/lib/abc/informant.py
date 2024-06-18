from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import typing

if typing.TYPE_CHECKING:
    from lib.abc.driver import DriverABC

"""
A Notitia informant has a single job, which is to wait for an investigator
to ask for information, then do its best to get that information.
They never go off on their own to find new information and they always
ensure the information provided back to the investigator is in the
agreed format.
"""

NOTITIA_DEPENDENCIES: typing.Dict


@dataclass
class InformantABC(ABC):
    department: typing.AnyStr = field(kw_only=True, default=None)
    name: typing.AnyStr = field(init=False)
    key: typing.AnyStr = field(init=False)
    type: typing.AnyStr = field(init=False, default="informant")

    driver: typing.Dict[typing.AnyStr, DriverABC] = field(
        init=True, kw_only=True, default=None
    )

    def sign_on(self) -> typing.Dict:
        pass

    @abstractmethod
    async def enquire(self, **kwargs):
        pass

    @abstractmethod
    async def inform(self):
        pass
