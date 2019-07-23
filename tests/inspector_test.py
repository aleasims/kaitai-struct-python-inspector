import os
import sys

script_path = os.path.realpath(__file__)
tests_dir = os.path.dirname(script_path)
root_dir = os.path.dirname(tests_dir)
sys.path.insert(0, root_dir)


def test_inspector():
    from inspector import Inspector

    test_file = os.path.join(tests_dir, 'data/sample.png')

    i = Inspector('', test_file)

    print('OK')
    return i


if __name__ == "__main__":
    i = test_inspector()
