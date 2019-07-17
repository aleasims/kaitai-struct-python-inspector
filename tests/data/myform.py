# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
import collections


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Myform(KaitaiStruct):
    SEQ_FIELDS = ["length", "body", "post"]
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._debug = collections.defaultdict(dict)

    def _read(self):
        self._debug['length']['start'] = self._io.pos()
        self.length = self._io.read_u4le()
        self._debug['length']['end'] = self._io.pos()
        self._debug['body']['start'] = self._io.pos()
        self.body = (self._io.read_bytes(self.length)).decode(u"utf8")
        self._debug['body']['end'] = self._io.pos()
        self._debug['post']['start'] = self._io.pos()
        self.post = (self._io.read_bytes_full()).decode(u"utf8")
        self._debug['post']['end'] = self._io.pos()


