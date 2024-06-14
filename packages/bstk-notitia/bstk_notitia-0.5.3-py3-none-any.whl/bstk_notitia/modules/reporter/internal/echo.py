from dataclasses import dataclass, field
import typing
from bstk_notitia.lib.abc.reporter import ReporterABC

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "null",
        "required": True,
    },
}


@dataclass
class NotitiaModule(ReporterABC):
    name = "Internal Echo Reporter"
    key = "internal/echo"

    timezone: typing.AnyStr = field(kw_only=True, default=None)

    async def receive(self, *args, **kwargs):
        if args:
            for _v in args:
                await self.publish(f"{_v}")

        if kwargs:
            for _k, _v in args:
                await self.publish(f"{_k}: {_v}")

    async def publish(self, data: str) -> typing.Any:
        print(data)
