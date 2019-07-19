import os
import sys

script_path = os.path.realpath(__file__)
tests_dir = os.path.dirname(script_path)
root_dir = os.path.dirname(tests_dir)
sys.path.insert(0, root_dir)


def test_inspector():
    from parsetree import RootNode
    from data.png import Png

    test_file = os.path.join(tests_dir, 'data/sample.png')

    with open(test_file, 'rb') as f:
        buf = f.read()

    parsed = Png.from_file(test_file)
    parsed._read()

    r = RootNode(buf, parsed, verbose=True)

    from inspector import Inspector
    i = Inspector('', '')

    dot = i.tree_to_dot(r)
    return r, i, dot


def run_tests():
    return test_inspector()


if __name__ == "__main__":
    r, i, dot = run_tests()
