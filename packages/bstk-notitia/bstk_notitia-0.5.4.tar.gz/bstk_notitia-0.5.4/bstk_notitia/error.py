class NotitiaError(Exception):
    pass


class NotitiaBootstrapError(NotitiaError):
    pass


class NotitiaInvalidDriverException(NotitiaError):
    pass


class NotitiaInvalidDriverParameter(NotitiaError):
    pass


class NotitiaUnsupportedDriverCall(NotitiaError):
    pass


class NotitiaInvalidCasePayloadException(NotitiaError):
    pass


class NotitiaPathExtensionWithoutSignature(NotitiaError):
    pass


class NotitiaPathExtensionMissingSignature(NotitiaError):
    pass


class NotitiaPathExtensionUnreferencedFile(NotitiaError):
    pass


class NotitiaPathExtensionFileSignatureInvalid(NotitiaError):
    pass


class NotitiaUnknownModule(NotitiaError):
    pass


class NotitiaMalformedModulePath(NotitiaError):
    pass


class NotitiaMissingModule(NotitiaError):
    pass


class NotitiaInvalidModulePath(NotitiaError):
    pass


class NotitiaUnknownObserver(NotitiaError):
    pass
