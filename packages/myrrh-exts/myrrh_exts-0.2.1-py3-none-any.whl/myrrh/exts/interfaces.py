import abc
import typing
import urllib.request

__all__ = ["IMyrrhExt", "IExtSession", "ExtSessionT"]


class IExtSession(abc.ABC):

    @abc.abstractmethod
    def query(self, query: str): ...

    @abc.abstractmethod
    def request(self, query: str, data: str | None = None): ...

    @abc.abstractmethod
    def close(self): ...


ExtSessionT = typing.TypeVar("ExtSessionT", bound=IExtSession)


def uri_rd(func):
    func.__access__ = "rd"
    return abc.abstractmethod(func)


def uri_wr(func):
    func.__access__ = "wr"
    return abc.abstractmethod(func)

def uri_wr_data(key):
    def wrap(func):
        func.__data__ = key
        return uri_wr(func)
    return wrap

class IMyrrhExt(abc.ABC, typing.Generic[ExtSessionT]):

    @abc.abstractmethod
    def basepath(self, path: str|None) -> str: ...

    @abc.abstractmethod
    def open(self, uri: str, *, req: urllib.request.Request | None = None) -> ExtSessionT: ...

    @abc.abstractmethod
    def extend(self, path: str, obj: typing.Any): ...


class IRootExt(IMyrrhExt):

    @property
    @abc.abstractmethod
    def dirs(self) -> dict[str, IMyrrhExt]: ...

    @abc.abstractmethod
    def getserv(self, path: str) -> IMyrrhExt | None: ...
