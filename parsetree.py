import kaitaistruct as ks
from enum import Enum


class Node:
    """Represents one segment in parse."""

    def __init__(self, name, start, end, root, parent, level=0):
        self.name = name
        self.start = start
        self.end = end
        self.root = root
        self.parent = parent
        self.level = level
        print('  ' * self.level + 'New node: {}'.format(self))

    @property
    def raw_value(self):
        """Sequence of bytes of this segment."""
        return self.root.get_value(self.start, self.end)

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
        print('  ' * self.level + 'Exploring node {}:'.format(self.name))
        self.childs = self._explore()

    def _explore(self):
        childs = []
        for index, obj in self._objects():
            name = self._child_name(index)
            start, end = self._markers(index)
            node = self._obj_to_node(obj, name, start, end, self.root, self)
            childs.append(node)
        return childs

    def _obj_to_node(self, obj, name, start, end, root, parent):
        if isinstance(obj, ks.KaitaiStruct):
            NodeClass = StructNode
        elif isinstance(obj, ValueNode.TYPES):
            NodeClass = ValueNode
        elif isinstance(obj, list):
            NodeClass = ArrayNode
        else:
            raise ValueError('Unknown object type: {}'.format(type(obj)))
        return NodeClass(obj, name, start, end, root, parent, level=self.level + 1)

    def _objects(self):
        raise NotImplementedError

    def _markers(self, index):
        raise NotImplementedError

    def _child_name(self, index):
        raise NotImplementedError


class StructNode(ExplorableNode):
    """Represents node of the subtype."""

    def _objects(self):
        for name in self.obj.SEQ_FIELDS:
            yield name, getattr(self.obj, name)

    def _markers(self, name):
        return self.obj._debug[name]['start'], self.obj._debug[name]['end']

    def _child_name(self, name):
        return name


class ArrayNode(ExplorableNode):
    """Represents node of array of subtype items."""

    def _objects(self):
        return enumerate(self.obj)

    def _markers(self, index):
        return self.parent.obj._debug[self.name]['arr'][index]['start'], \
                self.parent.obj._debug[self.name]['arr'][index]['end']

    def _child_name(self, index):
        return self.name + '[{}]'.format(index)


class RootNode(StructNode):
    def __init__(self, buffer, obj):
        self.buffer = buffer
        name = obj.__class__.__name__
        start, end = 0, len(self.buffer)
        super().__init__(obj, name, start, end, self, None)

    def get_value(self, start, end):
        return self.buffer[start:end]
