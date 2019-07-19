import os
import sys

script_path = os.path.realpath(__file__)
tests_dir = os.path.dirname(script_path)
root_dir = os.path.dirname(tests_dir)
sys.path.insert(0, root_dir)


def test_parsetree():
    import parsetree
    from data.png import Png
    test_file = os.path.join(tests_dir, 'data/sample.png')

    parsetree.parse_and_build(Png, test_file)

    parser = Png.from_file(test_file)
    parser._read()
    parsetree.build(parser)

    with open(test_file, 'rb') as fd:
        buffer = fd.read()
    parser = Png.from_bytes(buffer)
    parser._read()
    parsetree.build(parser)

    with open(test_file, 'rb') as fd:
        parser = Png.from_io(fd)
        parser._read()
        tree = parsetree.build(parser)

    print('OK')


if __name__ == "__main__":
    test_parsetree()
