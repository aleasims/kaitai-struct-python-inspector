"""Module responsible for building parse tree
from KaitaiStruct object, obtained after parsing.

Methods:
    build(struct) — build tree for provided structure.
    parse_and_build(ParserClass, buffer) — invokes parser for buffer
                                           and build tree for result.
"""


import io
from collections import namedtuple
from enum import Enum

import kaitaistruct as ks

Segment = namedtuple('Segment', ['start', 'end'])


class Node:
    """Represents one segment in parse."""

    PAD = '  '

    def __init__(self, name, segment, offset, root, parent,
                 level=0, verbose=False):
        self.name = name
        self.segment = segment
        self.offset = offset
        self.root = root
        self.parent = parent
        self.level = level
        self.verbose = verbose

        if self.verbose:
            self.log('New node: {}'.format(self))

    def log(self, msg):
        padding = self.PAD * self.level
        print(padding + msg)

    @property
    def start(self):
        return self.offset + self.segment.start

    @property
    def end(self):
        return self.offset + self.segment.end

    @property
    def raw_value(self):
        """Sequence of bytes of this segment."""
        return self.root.get_value(self.start, self.end)

    @property
    def size(self):
        return self.end - self.start

    def __repr__(self):
        return '{name}({type}) [{start}:{end}]'.format(
            name=self.name,
            type=self.__class__.__name__,
            start=self.start,
            end=self.end
        )


class ValueNode(Node):
    """Represents the lowest segment, which refers to a leaf in parse tree."""

    TYPES = (int, float, str, bytes, Enum)

    def __init__(self, value, *args, **kwargs):
        self._value = value
        super().__init__(*args, **kwargs)

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return '{name}({type}<{basetype}>) [{start}:{end}]'.format(
            name=self.name,
            type=self.__class__.__name__,
            basetype=self.value.__class__.__name__,
            start=self.start,
            end=self.end
        )


class ExplorableNode(Node):
    """Interface to nodes, which invokes exploration on init."""

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        super().__init__(*args, **kwargs)
        self.childs = self._explore()

    def _explore(self):
        childs = []
        for index, obj in self._objects():
            name = self._child_name(index)
            segment = Segment(**self._markers(index))
            offset = self._child_offset()
            node = self._obj_to_node(obj, name, segment, offset,
                                     self.root, self)
            childs.append(node)
        return childs

    def _obj_to_node(self, obj, name, segment, offset, root, parent):
        if isinstance(obj, ks.KaitaiStruct):
            NodeClass = StructNode
        elif isinstance(obj, ValueNode.TYPES):
            NodeClass = ValueNode
        elif isinstance(obj, list):
            NodeClass = ArrayNode
        else:
            raise ValueError('Unknown object type: {}'.format(type(obj)))

        return NodeClass(obj, name, segment, offset, root, parent,
                         level=self.level + 1, verbose=self.verbose)

    def _objects(self):
        raise NotImplementedError

    def _markers(self, index):
        raise NotImplementedError

    def _child_name(self, index):
        raise NotImplementedError

    def _child_offset(self):
        raise NotImplementedError


class StructNode(ExplorableNode):
    """Represents node of the subtype."""

    def _objects(self):
        for name in self.obj.SEQ_FIELDS:
            yield name, getattr(self.obj, name)

    def _markers(self, name):
        markers = self.obj._debug[name].copy()
        if 'arr' in markers:
            del markers['arr']
        return markers

    def _child_name(self, name):
        return name

    def _child_offset(self):
        if isinstance(self.parent, StructNode):
            if self.obj._io != self.parent.obj._io:
                return self.start
        return self.offset


class ArrayNode(ExplorableNode):
    """Represents node of array of subtype items."""

    def _objects(self):
        return enumerate(self.obj)

    def _markers(self, index):
        return self.parent.obj._debug[self.name]['arr'][index]

    def _child_name(self, index):
        return self.name + '[{}]'.format(index)

    def _child_offset(self):
        return self.offset


class RootNode(StructNode):
    def __init__(self, buffer, obj, verbose=False):
        self.buffer = buffer
        name = obj.__class__.__name__
        segment = Segment(0, len(self.buffer))
        offset = 0
        super().__init__(obj, name, segment, offset,
                         root=self, parent=None, verbose=verbose)

    def get_value(self, start, end):
        return self.buffer[start:end]


def build(struct, verbose=False):
    """Interface method, shorthand for RootNode()."""

    _io = struct._io._io
    if isinstance(_io, io.BytesIO):
        buffer = _io.getbuffer().tobytes()
    elif isinstance(_io, io.BufferedReader):
        with open(struct._io._io.name, 'rb') as f:
            buffer = f.read()
    else:
        raise TypeError('Unsupported stream type')

    return RootNode(buffer, struct, verbose)


def parse_and_build(ParserClass, path, verbose=False):
    """Interface method, invokes parser for buffer."""

    struct = ParserClass.from_file(path)
    struct._read()
    return build(struct, verbose)
