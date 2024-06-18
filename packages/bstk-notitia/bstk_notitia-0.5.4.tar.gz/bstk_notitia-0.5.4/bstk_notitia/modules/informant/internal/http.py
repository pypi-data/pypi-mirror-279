from datetime import datetime, UTC
from bstk_notitia.lib.abc.informant import InformantABC

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "null",
        "required": True,
    },
}


class NotitiaModule(InformantABC):
    name = "Internal HTTP Informant"
    key = "internal/http"

    async def enquire(self):
        return datetime.now(tz=UTC)

    async def inform(self):
        pass
