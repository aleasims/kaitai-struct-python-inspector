import base64
import json
from enum import Enum
from queue import Queue

from graphviz import Digraph

from kspyspector import parsetree


class NodeType(Enum):
    ValueNode = 0  # LEAF
    StructNode = 1  # STRUCTURE
    ArrayNode = 2  # SEQUENCE
    RootNode = 3  # ROOT
    VariantNode = 4  # VARIANT


class Inspector:
    def __init__(self, ksy, bin_path, ommit_empty=False, verbose=False):
        self.ksy = ksy
        self.parser = self.ksy.compile()
        self.spec = self.ksy.interpret()

        self.bin_path = bin_path
        self.ommit_empty = ommit_empty
        self.verbose = verbose

    def parse(self):
        self.struct = self.parser.from_file(self.bin_path)
        self.struct._read()

    def build(self):
        self.tree = parsetree.build(self.struct, self.ommit_empty,
                                    self.verbose)

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

    def to_trawl(self):
        def _to_trawl(node, **kwargs):
            """Recursive callable."""
            tjson = kwargs.copy()
            childs = getattr(node, 'childs', [])
            if childs:
                tjson['fields'] = {}
                for i, child in enumerate(childs):
                    args = {
                        'position': i,
                        'length': child.size,
                        'offset': child.start,
                        'type': getattr(NodeType,
                                        child.__class__.__name__).value
                    }
                    if isinstance(child, parsetree.ValueNode):
                        args['interpreted_value'] = str(child.value)
                        args['value_type'] = child.value.__class__.__name__
                    child_json = _to_trawl(child, **args)
                    tjson['fields'][child.name] = child_json
            return tjson

        return json.dumps({'format': _to_trawl(self.tree,
                                               position=0,
                                               offset=0,
                                               length=self.tree.size,
                                               type=NodeType.RootNode.value),
                           'meta': {
            'generic': False,
            'complete_buffer': True,
            'buffer': base64.b64encode(self.tree.buffer).decode()
        }
        })
