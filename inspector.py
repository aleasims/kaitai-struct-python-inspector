import functools
import json
from queue import Queue

from graphviz import Digraph

import parsetree
import ksy

TRAWL_TYPES = {
    'RootNode': 'ROOT',
    'StructNode': 'STRUCTURE',
    'ValueNode': 'LEAF',
    'ArrayNode': 'SEQUENCE'
}


def with_tree_only(func):
    """Checks persistence of `tree` attribute.

    Only for methods.
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'tree'):
            raise AttributeError('No tree builded.')
        return func(self, *args, **kwargs)

    return wrapper


class Inspector:
    def __init__(self, ksy_path, bin_path, verbose=False):
        self.ksy_path = ksy_path
        self.bin_path = bin_path
        self.verbose = verbose
        self.ParserClass = ksy.compile(self.ksy_path, verbose=self.verbose)
        self.tree = parsetree.parse_and_build(self.ParserClass,
                                              self.bin_path,
                                              self.verbose)

    @with_tree_only
    def to_dot(self):
        dot = Digraph()
        targets = Queue()
        targets.put(self.tree.root)
        while not targets.empty():
            target = targets.get()
            childs = getattr(target, 'childs', [])
            for child in childs:
                target_id = str(target).replace(':', '-')
                child_id = str(child).replace(':', '-')
                dot.edge(target_id, child_id)
                targets.put(child)
        return dot.source

    @with_tree_only
    def to_trawl(self):
        def _to_trawl(node, **kwargs):
            """Recursive callable."""
            json = kwargs.copy()
            childs = getattr(node, 'childs', [])
            if childs:
                json['fields'] = {}
                for i, child in enumerate(childs):
                    args = {
                        'position': i,
                        'length': child.size,
                        'offset': child.start,
                        'type': TRAWL_TYPES[child.__class__.__name__]
                    }
                    if isinstance(child, parsetree.ValueNode):
                        args['interpreted_value'] = str(child.value)
                        args['value_type'] = child.value.__class__.__name__
                    child_json = _to_trawl(child, **args)
                    json['fields'][child.name] = child_json
            return json

        return {self.tree.name: _to_trawl(self.tree,
                                          position=0,
                                          offset=0,
                                          length=self.tree.size,
                                          type=TRAWL_TYPES['RootNode'])}
