import pathlib
import typing
import urllib.parse
import urllib.request

from .interfaces import IExtSession

_T = typing.TypeVar("_T")
_ST = typing.TypeVar("_ST")


def singleton(cls_: typing.TypeAlias = _T) -> type[_T]:

    class _s(cls_, typing.Generic[_ST]):
        __instance__: cls_ = None

        def __new__(_s, *a, **kwa) -> cls_:
            if _s.__instance__ is None:
                _s.__instance__ = cls_(*a, **kwa)

            return _s.__instance__

    _s.__name__ = cls_.__name__
    _s.__doc__ = cls_.__doc__

    return _s


class URI:
    def __init__(self, uri, *, prefix: str = ""):

        if uri.startswith(":"):
            uri = "null" + uri

        if ":" not in uri:
            uri = "null:" + uri

        uri = urllib.parse.unquote_plus(uri)
        uri, frag = urllib.parse.urldefrag(uri)

        self._uri_result = self._urlsplit(uri, prefix)

        self._default_frag = frag

    def __str__(self):
        return self._uri_result.geturl()

    def _urlsplit(self, uri: str, prefix: str = ""):

        i = uri.find(":")

        scheme_, uri_ = (uri[:i], uri[i + 1 :]) if i > 0 else (uri, "")

        if scheme_.startswith("."):
            scheme_ = prefix + scheme_

        result = urllib.parse.urlsplit(uri_, scheme=scheme_)

        return result

    @property
    def uri(self):
        return str(self)

    @property
    def split(self):
        return self._uri_result

    @property
    def path(self) -> str:
        return self.split.path

    def joinpath(self, path:str| pathlib.PurePosixPath) -> "URI":
        path_ = pathlib.PurePosixPath(self.path).joinpath(path)
        self.path = path_
        return self
        
    @path.setter
    def path(self, path: str | pathlib.PurePosixPath):
        self._uri_result = self._uri_result._replace(path=str(path))

    @property
    def scheme(self):
        return self._uri_result.scheme

    @scheme.setter
    def scheme(self, scheme: str):
        self._uri_result = self._uri_result._replace(scheme=str(scheme))

    @property
    def base(self):
        return self._uri_result._replace(query="", fragment="").geturl()

    @property
    def fragment(self):
        return self._uri_result.fragment

    def frag(self, name: str | None = None):

        if name is None:
            name = self._default_frag

        return self._uri_result._replace(fragment=name).geturl()

    @property
    def request(self):
        return urllib.request.Request(self.uri)


class UriFile:
    def __init__(self, session: IExtSession, query: str):
        self.session = session
        self._query = query
        self._close = False

    def __enter__(self):
        return self

    def __exit__(self, *a, **kwa):
        self.session.close()

    @property
    def closed(self):
        return self._closed

    def read(self, count=1):
        resps = list()

        for _ in range(count):

            resp = self.session.query(self._query)

            if not resp:
                break

            resps.append(resp)

        return resps

    def write(self, data):
        return self.session.request(self._query, data)

    def get(self, query):
        return self.session.query(query)

    def push(self, query, data):
        return self.session.request(query, data)
