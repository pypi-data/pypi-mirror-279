from .notitia import Notitia, Loader
from .error import (
    NotitiaError,
    NotitiaInvalidDriverException,
    NotitiaInvalidCasePayloadException,
    NotitiaPathExtensionWithoutSignature,
    NotitiaPathExtensionMissingSignature,
    NotitiaPathExtensionUnreferencedFile,
    NotitiaPathExtensionFileSignatureInvalid,
    NotitiaUnknownModule,
    NotitiaMalformedModulePath,
)

__name__ = "bstk_notitia"
__package__ = __name__
__all__ = [
    "Notitia",
    "NotitiaError",
    "NotitiaInvalidDriverException",
    "NotitiaInvalidCasePayloadException",
    "NotitiaPathExtensionWithoutSignature",
    "NotitiaPathExtensionMissingSignature",
    "NotitiaPathExtensionUnreferencedFile",
    "NotitiaPathExtensionFileSignatureInvalid",
    "NotitiaUnknownModule",
    "NotitiaMalformedModulePath",
]

import os

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_PATHS = [
    "modules",
]
MODULE_TYPES = [
    "driver",
    "informant",
    "investigator",
    "observer",
    "reporter",
]

Notitia._module_loader = Loader(MODULE_DIR, MODULE_PATHS, MODULE_TYPES)
