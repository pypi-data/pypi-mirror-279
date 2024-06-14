from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, UTC
from decimal import Decimal, ROUND_HALF_UP
import typing
from uuid import uuid4
import simplejson

from bstk_notitia.lib.abc.reporter import ReporterABC

if typing.TYPE_CHECKING:
    from bstk_notitia.modules.driver.mongodb import (
        NotitiaModule as MongoDBDriver,
        DriverABC,
    )

NOTITIA_DEPENDENCIES = {
    "driver": {
        "type": "mongodb",
        "required": True,
    },
}


@dataclass
class NotitiaModule(ReporterABC):
    name = "Internal Notitia Case Reporter"
    key = "internal/notitia_case"

    if typing.TYPE_CHECKING:
        driver: typing.Dict[str, typing.Union[MongoDBDriver, DriverABC]]

    collection: typing.AnyStr = field(kw_only=True, default=None)

    async def receive(
        self,
        action: str,
        record: typing.Dict,
        data: typing.Optional[
            typing.Union[typing.List[typing.Dict], typing.Dict]
        ] = None,
    ) -> typing.Union[bool, str, typing.List[str]]:
        if action not in ("clone", "new"):
            return False
        _cases = []

        if data is None:
            data = {"number": None}

        if not isinstance(data, list):
            data = [data]

        for _entry in data:
            _entry["number"] = str(uuid4())
            _entry["assigned_investigator"] = None
            _entry["created_at"] = datetime.now(tz=UTC)
            _entry["updated_at"] = None
            _entry["closed_at"] = None

            if action == "clone":
                _entry["log"] = [
                    {
                        "type": "clone",
                        "module": "notitia",
                        "date": _entry["created_at"],
                    }
                ]
            else:
                _entry["log"] = [
                    {
                        "type": "created",
                        "module": "notitia",
                        "date": _entry["created_at"],
                    }
                ]

            _new_case = {**simplejson.loads(self.json_encode(record)), **_entry}
            if "_id" in _new_case:
                del _new_case["_id"]

            print(f"{self.key} created {action} case {_new_case['number']}")
            _res = await self.publish(_new_case)
            if not _res:
                continue
            _cases.append(_res)

        if not len(_cases):
            return False

        return _cases if len(_cases) > 1 else _cases[0]

    async def publish(self, case_data: typing.Dict):
        res = (
            await self.driver["mongodb"]
            .get_collection(self.collection)
            .insert_one(document=case_data)
        )

        if hasattr(res, "inserted_id") and res.inserted_id:
            return res.inserted_id

        return False

    def json_encode(self, value: typing.Any) -> str:
        """
        A consistency layer around json.dumps.
        (you usually just get the .__str__() output)
        Handles:
            * Date/Datetime
            * UUID
            * Decimals
        Do _not_ use this if you're targeting mongodb, use the BSON methods instead.
        """
        return simplejson.dumps(value, default=self.json_convert, use_decimal=True)

    def json_convert(self, elem: typing.Any) -> str:
        if isinstance(elem, object):
            if hasattr(elem, "_to_json"):
                return elem._to_json()
            if hasattr(elem, "isoformat"):
                return elem.isoformat()
            if hasattr(elem, "strftime"):
                return elem.strftime("%Y-%m-%d")
            if hasattr(elem, "to_decimal"):
                elem = elem.to_decimal()
            if hasattr(elem, "quantize"):
                return float(elem.quantize(Decimal("1.0000"), rounding=ROUND_HALF_UP))
            if hasattr(elem, "value"):
                return elem.value

        try:
            return str(elem)
        except Exception:
            return None
