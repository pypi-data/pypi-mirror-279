import functools
import typing

import warnings
import traceback
import pathlib
import abc

import urllib.request

import importlib
import importlib.metadata


from .errors import ExtendTypeError, InvalidPath, URIOpenError
from .interfaces import IRootExt, IExtSession, IMyrrhExt, uri_rd
from .misc import URI, singleton, UriFile
from .client import ExtClient
from .protocol import MyrrhExtBase, StdExtSession


class IRootSession(IExtSession):

    @uri_rd
    @abc.abstractmethod
    def list(self) -> list[str]: ...  #


class RootSession(StdExtSession, IRootSession, IExtSession):

    def __init__(self, dirs):
        super().__init__(IRootSession)
        self.dirs = dirs

    def list(self) -> list[str]:
        return list(self.dirs)


class Root(MyrrhExtBase, IRootExt):

    def getserv(self, path: str) -> IMyrrhExt | None:
        dirs = self.dirs

        if path in dirs:
            return dirs.get(str(path))

        for p in pathlib.PurePosixPath(path).parents:
            serv = dirs.get(str(p))
            if serv:
                return serv

        return None

    def open(self, uri: str, *, req: urllib.request.Request | None = None):
        path = URI(uri).path

        if path == self._path:
            return RootSession(path)

        serv = self.getserv(path)

        if not serv:
            raise InvalidPath(path)

        return serv.open(uri, req=req)

    @functools.cached_property
    def dirs(self):
        self._dirs = dict()
        return self._dirs

    def extend(self, path: str, obj: typing.Any):

        serv = self.getserv(path)

        if serv:
            serv.extend(path, obj)
            return

        if not path.startswith("/"):
            raise InvalidPath(path)

        if callable(obj):
            obj = obj()

        if obj is None:
            self.dirs[path] = None

        elif not isinstance(obj, IMyrrhExt):
            raise ExtendTypeError(obj, path)

        else:
            obj.basepath(path)
            self.dirs[path] = obj


class PathHandler(urllib.request.BaseHandler):

    def __init__(self, scheme: str, root: IRootExt):
        self.root = root
        setattr(self, f"{scheme}_open", self._open)

    def _validate_req(self, req):
        path = URI(req.full_url).path
        return self.root.getserv(path)

    def _open(self, req: urllib.request.Request) -> UriFile | ExtClient | None:

        serv = self._validate_req(req)

        if not serv:
            return None

        if req.fragment == "client":  # type: ignore[attr-defined]
            client = ExtClient[IExtSession](serv)
            client.seturi(req.full_url)
            return client

        session = serv.open(req.full_url, req=req)

        if session:
            return UriFile(session, URI(req.full_url).split.query)

        return None

    def _serv(self, req: urllib.request.Request) -> IMyrrhExt:
        serv = self._validate_req(req)
        return serv

    def append(self, path: str, obj):
        self.root.extend(path, obj)


@singleton
class Registry:

    _handlers: dict[str, PathHandler] = {}
    failed: set[str] = set()
    loaded: set[str] = set()

    opener = urllib.request.OpenerDirector()

    def _new_handler(self, scheme: str, *, root: IRootExt | None = None):
        ep = None

        if not root:
            eps = importlib.metadata.entry_points(group=scheme, name=".")
            ep = eps[0] if eps else None
            root = ep.load()() if ep else Root()

        self._handlers[scheme] = PathHandler(scheme, root)
        self.opener.add_handler(self._handlers[scheme])

        if ep:
            self.loaded.add(f"{ep.group}:{ep.name}")

        return self._handlers[scheme]

    def _get_handler(self, scheme, *, root: IRootExt | None = None):
        handler = self._handlers.get(scheme)
        if not handler:
            handler = self._new_handler(scheme, root=root)

        return handler

    def _load(self, group: str, path: str, handler: PathHandler | None = None):

        handler = self._get_handler(group) if not handler else handler

        ep = importlib.metadata.entry_points(group=group, name=path)

        if not ep:
            handler.append(path, None)
            return

        handler.append(ep[0].name, ep[0].load())
        self.loaded.add(f"{ep[0].group}:{ep[0].name}")

    def _extend(self, scheme, path, obj):
        handler = self._get_handler(scheme)

        for p in reversed(pathlib.PurePosixPath(path).parents):
            if str(p) not in handler.root.dirs:
                self._load(scheme, str(p), handler)

        handler.append(path, obj)

    def findall(self, uri: str | None = None) -> list[str]:
        founds = []
        uri_ = URI(uri)
        for group, eps in importlib.metadata.entry_points().items():
            if not uri or group == uri_.scheme:
                for ep in eps:
                    if not uri_.path or ep.name.startswith(uri_.path):
                        founds.append(f"{ep.group}:{ep.name}")

        return founds

    def load(self, group: str, *, path: str = ""):
        if not path:
            group, _, path = group.partition(":")

        paths = {ep.name: ep for ep in importlib.metadata.entry_points(group=group)}
        subpaths = [p for p in paths if p.startswith(path)]

        for p in (*reversed(pathlib.PurePosixPath(path).parents), path, *subpaths):
            p_ = str(p)
            if p_ in paths:
                ep = paths[p_]
                key = f"{ep.group}:{ep.name}"
                if key not in self.loaded:
                    try:
                        self._extend(ep.group, ep.name, ep.load())
                        self.loaded.add(key)
                    except Exception as e:
                        warnings.warn(f"{''.join(traceback.format_tb(e.__traceback__))}\nFailed to load {ep.group}:{ep.name}, this extension will be unavailable: {str(e)}")
                        self.failed.add(key)

    def load_uri(self, uri: str):
        uri_ = URI(uri)
        ext = f"{uri_.scheme}:{uri_.path}"
        if ext not in self.loaded:
            self.load(uri_.scheme, path=uri_.path)

    def open(self, uri: str, data: typing.Any = None, timeout: float | None = None):
        self.load_uri(uri)

        result = self.opener.open(uri, data, timeout)

        if not result:
            raise URIOpenError("no service found")

        return result

    def client(self, uri: str) -> ExtClient:
        self.load_uri(uri)

        result = self.opener.open(URI(uri).frag("client"))
        if not result:
            raise URIOpenError(f"no service found for {uri}")

        return result
    
    def extend(self, uri: str, obj):
        uri_ = URI(uri)
        self._extend(uri_.scheme, uri_.path, obj)
