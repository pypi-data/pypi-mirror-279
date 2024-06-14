from datetime import datetime, UTC, timezone
import dateparser
import typing
from bstk_notitia.lib.abc.informant import InformantABC

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "null",
        "required": True,
    },
}


class NotitiaModule(InformantABC):
    name = "Internal DateTime Informant"
    key = "internal/datetime"

    async def enquire(self, input: typing.Optional[str] = None):
        if not input:
            return datetime.now(tz=UTC)
        return self.parse(input)

    async def inform(self):
        pass

    def parse(self, date_string: str, tz: timezone = None) -> datetime:
        _date = dateparser.parse(date_string)

        if tz:
            return _date.astimezone(tz=tz)

        return _date
