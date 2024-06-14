import os
import re
from pathlib import Path
import importlib.util
from types import ModuleType
import typing

from .error import (
    NotitiaError,
    NotitiaInvalidModulePath,
    NotitiaMalformedModulePath,
    NotitiaMissingModule,
    NotitiaPathExtensionFileSignatureInvalid,
    NotitiaPathExtensionMissingSignature,
    NotitiaPathExtensionUnreferencedFile,
    NotitiaPathExtensionWithoutSignature,
    NotitiaUnknownModule,
)

NOTITIA_MODULE_DEPLIST = {
    "investigator": (
        "driver",
        "observer",
        "informant",
        "reporter",
    ),
    "observer": ("driver",),
    "informant": ("driver",),
    "reporter": ("driver",),
    "driver": (),
}


class Loader:
    module_paths: typing.Optional[typing.List[typing.AnyStr]] = None
    _processed_paths: typing.List[typing.AnyStr] = None
    _module_path_lookup: typing.Dict[typing.AnyStr, typing.AnyStr] = None

    modules: typing.Dict[typing.AnyStr, typing.List[typing.AnyStr]] = None
    _modules: typing.Dict[typing.AnyStr, typing.Dict[typing.AnyStr, ModuleType]] = None

    module_types: typing.List[typing.AnyStr] = None

    signing_key: typing.Optional[typing.AnyStr] = None
    untrusted_paths: typing.Optional[typing.List[typing.AnyStr]] = None

    def __init__(self, base_dir, module_paths=None, module_types=None):
        self.base_dir = Path(base_dir)
        if module_paths is None:
            return

        self.module_paths = module_paths
        self.untrusted_paths = []
        self._processed_paths = []

        self.modules = {}
        self._modules = {}
        self._module_path_lookup = {}

        if module_types is None:
            return

        self.module_types = module_types
        self._collect_modules_from_paths()

    def get_module_types(self):
        return list(self.modules.keys())

    def list_modules(self, type: str = None):
        if type is None:
            return self.modules

        return self.modules.get(type, False)

    def get_module(self, type: str, code: str):
        if type not in self._modules:
            return False

        return self._modules[type].get(code, False)

    def add_paths(self, paths: typing.List[typing.AnyStr]):
        for path in paths:
            path = Path(path)
            if not path.exists() or not path.is_dir():
                continue

            try:
                self.base_dir.parent.relative_to(path)
            except ValueError:
                if not self.signing_key:
                    raise NotitiaPathExtensionWithoutSignature(
                        "Refusing to include an external module path without a signature"
                    )
                self.untrusted_paths.append(path)
                continue

            self.module_paths.append(path)

        self._collect_modules_from_paths()

    def _collect_modules_from_paths(self):
        if self.module_paths is None:
            return False

        for module_path in [*self.module_paths, *self.untrusted_paths]:
            module_path = Path(
                os.path.join(self.base_dir, module_path)
                if module_path not in self.untrusted_paths
                else module_path
            )
            if (
                not module_path.exists()
                or not module_path.is_dir()
                or module_path in self._processed_paths
            ):
                continue

            module_files = list(module_path.glob("**/*.py"))
            if not len(module_files):
                continue

            if module_path in self.untrusted_paths:
                try:
                    self._validate_signature(module_path, module_files)
                except (
                    NotitiaPathExtensionWithoutSignature,
                    NotitiaPathExtensionMissingSignature,
                    NotitiaPathExtensionUnreferencedFile,
                    NotitiaPathExtensionFileSignatureInvalid,
                ) as e:
                    self.untrusted_paths.remove(module_path)
                    raise e

            self._collect_modules_from_path(module_path, module_files)

            self._processed_paths.append(module_path)

    def _collect_modules_from_path(
        self,
        module_path: Path,
        module_files: typing.List[Path],
    ):
        for module_file in module_files:
            _mod_path = module_file.relative_to(module_path)

            if len(_mod_path.parts) > 3 or len(_mod_path.parts) < 2:
                raise NotitiaMalformedModulePath()

            _mod_type = _mod_path.parts[0]
            if _mod_type not in self.module_types:
                continue

            if _mod_type not in self.modules:
                self.modules[_mod_type] = []

            module_name = re.sub(r"\.py$", "", module_file.name)
            if module_name[0:1] == "_":
                # It's a valid module that's passed signature checks - but it's not executable, so we don't load it
                continue

            if module_file.parent.name != _mod_type:
                module_name = f"{module_file.parent.name}/{module_name}"

            self.modules[_mod_type].append(module_name)
            self._module_path_lookup[f"{_mod_type}/{module_name}"] = module_file

    def load_module(self, module_type: typing.AnyStr, module_name: typing.AnyStr):
        if self.module_paths is None:
            return False

        if (
            module_type not in self.modules
            or module_name not in self.modules[module_type]
        ):
            raise NotitiaUnknownModule()

        if module_type not in self._modules:
            self._modules[module_type] = {}

        if module_name in self._modules[module_type]:
            return

        _mod_name = f"{module_type}/{module_name}"
        if _mod_name not in self._module_path_lookup:
            raise NotitiaMissingModule()

        module_file = self._module_path_lookup[_mod_name]

        if not os.path.exists(module_file):
            raise NotitiaInvalidModulePath()

        _mod = __class__._import_module(_mod_name, module_file)
        self._modules[module_type][module_name] = _mod
        if not _mod:
            return

        self._load_module_deps(module_type, _mod)

    def _load_module_deps(self, module_type: str, module: ModuleType):
        acceptable_deps = NOTITIA_MODULE_DEPLIST[module_type]

        _deps: typing.Dict[str, typing.Union[typing.List, typing.Dict]] = getattr(
            module, "NOTITIA_DEPENDENCIES", {}
        )
        for _type, _deplist in _deps.items():
            if _type not in acceptable_deps:
                raise NotitiaError(
                    f"{module_type} modules cannot depend on `{_type}` modules"
                )

            if isinstance(_deplist, dict):
                _deplist = [_deplist]

            for _dep in _deplist:
                try:
                    self.load_module(_type, _dep["type"])
                except NotitiaError as ex:
                    if "required" in _dep and _dep["required"]:
                        raise ex

    def _validate_signature(self, path: Path, files: typing.List[Path]):
        if not self.signing_key:
            raise NotitiaPathExtensionWithoutSignature(
                "Refusing to process - no signature provided"
            )
        sig_file = Path(path, ".verify")
        if not sig_file.exists():
            raise NotitiaPathExtensionMissingSignature(
                "Refusing to process - no .verify file found"
            )

        _signatures = {}
        with sig_file.open("r") as _f:
            for _l in _f.readlines():
                _l = _l.strip().split(":", 1)
                _signatures[_l[0]] = _l[1]

        import hashlib
        import hmac

        for _file in files:
            _fileref = str(_file.relative_to(path))

            if _fileref not in _signatures:
                raise NotitiaPathExtensionUnreferencedFile("Missing signature for file")

            _contents = _file.read_text()
            _signature = hmac.new(
                self.signing_key.encode(), _contents.encode(), hashlib.sha256
            ).hexdigest()

            if _signature != _signatures[_fileref]:
                raise NotitiaPathExtensionFileSignatureInvalid(
                    f"Signature verification failed for {_fileref}"
                )

    @staticmethod
    def _import_module(name: str, source: Path) -> ModuleType:
        try:
            spec = importlib.util.spec_from_file_location(
                "notitia_module." + name.replace("/", "."), source
            )
            loader = importlib.util.LazyLoader(spec.loader)
            spec.loader = loader
            module = importlib.util.module_from_spec(spec)
            loader.exec_module(module)
            if hasattr(module, "BaseNotitiaModule"):
                return False

            if not hasattr(module, "NotitiaModule"):
                raise ValueError(
                    f"Invalid module {module} - NotitiaModule class not defined"
                )
            return module

        except Exception as e:
            print(f"failed to load module {source} // {str(e)}")
            return False
