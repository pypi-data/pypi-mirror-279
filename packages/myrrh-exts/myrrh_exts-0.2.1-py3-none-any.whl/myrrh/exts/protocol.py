import abc
import urllib.parse
import json
import typing

from .interfaces import IExtSession, IMyrrhExt
from .errors import InvalidRequest


class StdExtSession(IExtSession):

    def __init__(self, interface: type[abc.ABC]):
        self.queries = frozenset(m for m in interface.__abstractmethods__ if not m.startswith("_") and m not in IExtSession.__abstractmethods__)
        self.rd_queries = frozenset(m for m in self.queries if getattr(getattr(interface, m), "__access__", "").startswith("rd"))
        
        for m in self.queries:
            method = getattr(self, m)
            __data__ = getattr(getattr(interface, m), "__data__", "data") 
            __access__ = getattr(getattr(interface, m), "__access__", "")
            setattr(method.__func__, '__data__', __data__)
            setattr(method.__func__, '__access__', __access__)

    def _method(self, attr):
        m_name = attr.pop("", None)

        if m_name is None:
            raise InvalidRequest(f"no method")

        if m_name in self.queries:
            return getattr(self, m_name)

        if m_name == "__proto__":
            return getattr(self, m_name)

        raise AttributeError(f'"{m_name}" is not a valid method name')

    def _attr(self, attr):
        attrs = dict()
        for name, value in attr.items():
            if name.endswith("[js]"):
                value = json.loads(value)
                name = name[: len["[js]"]]
            attrs[name] = value
        return attrs

    def close(self):
        pass

    def query(self, query: str):
        attr = dict(urllib.parse.parse_qsl(query))
        method = self._method(attr)
        attrs = self._attr(attr)

        if method.__access__.startswith("rd"):
            return method(**attrs)

    def request(self, query: str, data: typing.Any | None = None):
        attr = dict(urllib.parse.parse_qsl(query))
        method = self._method(attr)
        if method.__access__.startswith("rd"):
            return self.query(query)

        attrs = self._attr(attr)
        attrs[method.__data__] = data
        return method(**attrs)

    def __proto__(self):
        return list(m for m in self.queries)

    __proto__.__access__ = 'rdonly'
    

class MyrrhExtBase(IMyrrhExt):
    _path = '.'
    
    def basepath(self, path:str|None=None) :
        if path:
            self._path = path
            
        return self._path