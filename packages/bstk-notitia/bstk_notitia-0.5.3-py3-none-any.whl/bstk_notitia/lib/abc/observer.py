from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import typing

if typing.TYPE_CHECKING:
    from lib.abc.driver import DriverABC

"""
Observers are the initial source for all investigators. They
are unbiased and focus only on validating that the subject
information matches a fixed criteria.

An investigator will give an observer guidelines regarding
what kind of information it cares about, and the observer
will provide that back to the investigator once it sees
matching information.

Observers only exist when an investigator requests one and are
the only mechanism by which the system will start processing
information.

Investigators are inherently lazy, so if the observer reports
nothing, then the investigator will happily sleep forever.

If an observer relies on external information, (ie: queue entry,
data changes, etc), it needs to be aware that it is not the only
observer in the system, so it should track its own state, ensuring
that it doesn't report invalid or duplicate information, nor
prevent other observers from working with the source data.
"""

NOTITIA_DEPENDENCIES: typing.Dict


@dataclass
class ObserverABC(ABC):
    department: typing.AnyStr = field(kw_only=True, default=None)
    name: typing.AnyStr = field(init=False)
    key: typing.AnyStr = field(init=False)
    type: typing.AnyStr = field(init=False, default="observer")

    driver: typing.Dict[typing.AnyStr, DriverABC] = field(
        init=True, kw_only=True, default=None
    )

    def sign_on(self) -> typing.Dict:
        pass

    @abstractmethod
    async def glance(self, *args, **kwargs) -> bool:
        """Quickly review the input data and see whether this observe should be looking at the data"""
        pass

    @abstractmethod
    async def monitor(
        self, *args, **kwargs
    ) -> typing.Union[typing.Any, typing.AsyncGenerator[typing.Any, typing.Any]]:
        """With the given args, keep watch until there is something to report back with"""
        pass
