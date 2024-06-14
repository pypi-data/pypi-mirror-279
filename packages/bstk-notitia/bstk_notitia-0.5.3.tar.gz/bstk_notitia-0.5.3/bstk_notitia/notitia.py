from __future__ import annotations
from types import ModuleType
import typing

from .roster import Roster, RosterType


if typing.TYPE_CHECKING:
    from lib.abc.investigator import InvestigatorABC
    from lib.abc.observer import ObserverABC
    from lib.abc.informant import InformantABC
    from lib.abc.reporter import ReporterABC

from .loader import Loader
from .error import (
    NotitiaBootstrapError,
    NotitiaInvalidDriverException,
)


class Notitia:
    __slots__ = (
        "driver",
        "driver_settings",
        "department",
        "observers",
        "informants",
        "reporters",
        "investigators",
        "_module_loader",
        "_supported_drivers",
        "_code_signature",
        "_roster",
    )

    driver: typing.AnyStr
    driver_settings: typing.Dict
    department: typing.Optional[typing.AnyStr]
    observers: typing.Dict[typing.AnyStr, ObserverABC]
    informants: typing.Dict[typing.AnyStr, InformantABC]
    reporters: typing.Dict[typing.AnyStr, ReporterABC]
    investigators: typing.Dict[typing.AnyStr, InvestigatorABC]
    _module_loader: Loader
    _supported_drivers: typing.Set[typing.AnyStr]
    _code_signature: typing.Optional[typing.AnyStr]
    _roster: typing.Optional[Roster]

    def __init__(
        self,
        department: typing.Optional[typing.AnyStr] = None,
        code_signature: typing.Optional[typing.AnyStr] = None,
    ):
        self.department = department

        self.driver = None
        self.driver_settings = None
        self._roster = None

        self.observers = self._module_loader.list_modules("observer")
        self.informants = self._module_loader.list_modules("informant")
        self.reporters = self._module_loader.list_modules("reporter")
        self.investigators = self._module_loader.list_modules("investigator")
        self._supported_drivers = self._module_loader.list_modules("driver")
        self._code_signature = code_signature

    def set_driver(
        self,
        driver: typing.AnyStr,
        driver_settings: typing.Dict,
    ):
        if driver not in self._supported_drivers:
            raise NotitiaInvalidDriverException()

        self.driver = driver
        self.driver_settings = driver_settings

    def get_from_registry(
        self,
        type: typing.AnyStr,
        key: typing.AnyStr,
    ) -> ModuleType[InvestigatorABC, ObserverABC, InformantABC, ReporterABC]:
        return self._module_loader.get_module(type, key)

    def extend(self, paths: typing.List[typing.AnyStr]):
        self._module_loader.signing_key = self._code_signature
        self._module_loader.add_paths(paths)

    def enlist(
        self,
        observer: typing.Optional[typing.AnyStr] = None,
        informant: typing.Optional[typing.AnyStr] = None,
        reporter: typing.Optional[typing.AnyStr] = None,
        investigator: typing.Optional[typing.AnyStr] = None,
    ):
        if observer:
            if observer not in self.observers:
                raise ValueError("Invalid observer")
            self._module_loader.load_module("observer", observer)

        if informant:
            if informant not in self.informants:
                raise ValueError("Invalid informant")
            self._module_loader.load_module("informant", informant)

        if reporter:
            if reporter not in self.reporters:
                raise ValueError("Invalid reporter")
            self._module_loader.load_module("reporter", reporter)

        if investigator:
            if investigator not in self.investigators:
                raise ValueError("Invalid investigator")
            self._module_loader.load_module("investigator", investigator)

    def clock_on(
        self,
        investigator: str,
        investigator_params: typing.Optional[typing.Dict] = None,
        dependency_params: typing.Optional[
            typing.Dict[str, typing.Dict[str, typing.Dict]]
        ] = None,
        *args,
        **kwargs,
    ):
        if investigator not in self.investigators:
            raise ValueError("Invalid investigator")

        _mod = self.get_from_registry("investigator", investigator)
        if _mod is False:
            raise ValueError("Investigator not enlisted or failed to load")

        _obj = self._load_and_resolve_investigator(
            _mod,
            investigator_params=investigator_params,
            dependency_params=dependency_params,
        )
        self._add_to_roster(
            _obj,
            {"args": args, "kwargs": kwargs},
        )

    def _boot_investigator(
        self, investigator_module, investigator_params
    ) -> InvestigatorABC:
        _obj: InvestigatorABC = investigator_module.NotitiaModule(
            department=self.department
        )
        _obj.sign_on(**investigator_params)
        return _obj

    def _load_and_resolve_investigator(
        self,
        investigator_module: ModuleType[InvestigatorABC],
        investigator_params: typing.Optional[typing.Dict] = None,
        dependency_params: typing.Optional[
            typing.Dict[str, typing.Dict[str, typing.Dict]]
        ] = None,
    ):
        if not investigator_params:
            investigator_params = {}

        _deps = getattr(investigator_module, "NOTITIA_DEPENDENCIES", None)
        if not _deps:
            return self._boot_investigator(investigator_module, investigator_params)

        _modules = self._resolve_module_dependencies(_deps)

        for _mod_type, _mod_entries in _deps.items():
            if not isinstance(_mod_entries, list):
                _mod_entries = [_mod_entries]

            for _mod_config in _mod_entries:
                _mod_key = f"{_mod_type}/{_mod_config['type']}"
                if _mod_key not in _modules or not _modules[_mod_key]["module"]:
                    if _mod_config.get("required", True):
                        raise RuntimeError(
                            f"Failed to load required dependency {_mod_key}"
                        )
                    continue

        for _type in ("driver", "observer", "informant", "reporter"):
            self._resolve_investigator_params(
                _type, investigator_params, dependency_params, _modules, _deps
            )

        return self._boot_investigator(investigator_module, investigator_params)

    def _resolve_investigator_params(  # noqa C90
        self,
        dep_type: str,
        investigator_params: typing.Dict[str, typing.Dict],
        dependency_params: typing.Dict[str, typing.Dict],
        modules: typing.Dict[str, typing.Dict],
        deps: typing.Dict[str, typing.Dict],
    ):
        # driver must come first, because other modules may request the driver
        if dep_type not in deps:
            return

        _entries = deps[dep_type]
        if not isinstance(_entries, list):
            _entries = [_entries]

        _di = {}
        for _entry in _entries:
            _mod = modules[f"{dep_type}/{_entry['type']}"]
            if (
                dependency_params
                and dep_type in dependency_params
                and _entry["type"] in dependency_params[dep_type]
            ):
                _mod["params"].update(dependency_params[dep_type][_entry["type"]])

            _req_drivers = []
            if (
                dep_type != "driver"
                and "driver" in investigator_params
                and investigator_params["driver"]
            ):
                _req_drivers = getattr(_mod["module"], "NOTITIA_DEPENDENCIES", {}).get(
                    "driver", []
                )
                if _req_drivers and not isinstance(_req_drivers, list):
                    _req_drivers = [_req_drivers]

            if _req_drivers:
                if "params" not in _mod:
                    _mod["params"] = {}
                if "driver" not in _mod["params"]:
                    _mod["params"]["driver"] = {}

            for _req_driver in _req_drivers:
                _t = _req_driver["type"]
                if _t not in investigator_params["driver"]:
                    continue

                _mod["params"]["driver"][_t] = investigator_params["driver"][_t]

            _di[_entry["type"]] = self._load_resolve_module(
                _mod["module"], init_params=_mod["params"]
            )

        investigator_params[dep_type] = _di

    def _resolve_module_dependencies(
        self,
        _deps: typing.Dict,
        _modules: typing.Optional[typing.Dict[str, typing.Dict]] = None,
    ) -> typing.Dict[str, typing.Dict]:
        is_nested = True
        if not _modules:
            is_nested = False
            _modules = {}

        # First pass - load modules
        for _mod_type, _mod_entries in _deps.items():
            if not isinstance(_mod_entries, list):
                _mod_entries = [_mod_entries]

            for _mod_config in _mod_entries:
                _mod_key = f"{_mod_type}/{_mod_config['type']}"
                if _mod_key in _modules:
                    continue

                _modules[_mod_key] = {
                    "module": self.get_from_registry(_mod_type, _mod_config["type"]),
                    "params": _mod_config.get("params", {}),
                }

                _subdeps = getattr(
                    _modules[f"{_mod_type}/{_mod_config['type']}"],
                    "NOTITIA_DEPENDENCIES",
                    None,
                )
                if _subdeps:
                    self._resolve_module_dependencies(_subdeps, _modules)

        if is_nested:
            return

        return _modules

    def _load_resolve_module(
        self, _mod: ModuleType, init_params: typing.Optional[typing.Dict]
    ):
        try:
            return _mod.NotitiaModule(**init_params, department=self.department)
        except TypeError as ex:
            raise NotitiaBootstrapError(_mod.__file__) from ex

    def _add_to_roster(
        self, investigator: InvestigatorABC, startup_params: typing.Dict
    ):
        if not self._roster:
            self._roster = Roster()

        self._roster.add(
            investigator=investigator,
            startup_params=startup_params,
            type=RosterType.PERMANENT,
        )

    def get_roster(self) -> Roster:
        if not self._roster:
            raise Exception("Roster is empty")

        return self._roster
