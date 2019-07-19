from queue import Queue
from graphviz import Digraph


class Inspector:
    def __init__(self, ksypath, binpath):
        self.ksy_path = ksypath
        self.bin_path = binpath

        self.compile_ksy(self.ksy_path)

        self.build_tree()

    def compile_ksy(self, path):
        pass

    def build_tree(self):
        pass

    def tree_to_dot(self, tree):
        dot = Digraph()
        targets = Queue()
        targets.put(tree.root)
        while not targets.empty():
            target = targets.get()
            childs = getattr(target, 'childs', [])
            for child in childs:
                target_id = str(target).replace(':', ' ')
                child_id = str(child).replace(':', ' ')
                dot.edge(target_id, child_id)
                targets.put(child)
        return dot
