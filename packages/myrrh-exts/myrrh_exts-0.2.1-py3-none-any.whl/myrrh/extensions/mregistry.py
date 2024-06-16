import typing
import urllib.request
import urllib.error
import abc

from myrrh.exts.protocol import MyrrhExtBase, StdExtSession
from myrrh.exts.misc import URI, singleton
from myrrh.exts.errors import ReadOnlyPath, InvalidPath
from myrrh.exts.interfaces import ExtSessionT, IMyrrhExt, IExtSession, uri_rd

from myrrh.exts.registry import Registry


class IExtRegistrySession(IExtSession):

    @uri_rd
    @abc.abstractmethod
    def findall(self, prefix: str | None = None): ...

    @uri_rd
    @abc.abstractmethod
    def loaded(self): ...


@singleton
class ExtRegistrySession(StdExtSession, IExtRegistrySession, typing.Generic[ExtSessionT]):

    def __init__(self):
        super().__init__(interface=IExtRegistrySession)

    def findall(self, prefix: str | None = None):
        return Registry().findall(uri=prefix)

    def loaded(self):
        return list(Registry().loaded)


class ExtRegistry(MyrrhExtBase):

    def open(self, uri: str, *, req: urllib.request.Request | None = None) -> ExtRegistrySession:

        if URI(uri).path != self._path:
            raise InvalidPath(URI(uri).path)

        return ExtRegistrySession()


    def extend(self, path: str, obj: typing.Any):
        raise ReadOnlyPath(self._path)
