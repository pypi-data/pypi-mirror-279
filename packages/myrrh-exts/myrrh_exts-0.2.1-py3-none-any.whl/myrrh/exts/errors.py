import urllib.error
import typing


class ExtError(urllib.error.URLError): ...


class PathError(urllib.error.URLError): ...


class URIOpenError(urllib.error.URLError): ...


class InvalidRequest(urllib.error.URLError): ...


class ExtendTypeError(ExtError):
    def __init__(self, type: typing.Any, path: str | None = None) -> None:
        super().__init__(f"invalid extension type {type.__class__}", path)


class ReadOnlyPath(PathError):
    def __init__(self, path: str | None = None) -> None:
        super().__init__("readonly directory", path)


class InvalidPath(PathError):
    def __init__(self, path: str | None = None) -> None:
        super().__init__("invalid path", path)
