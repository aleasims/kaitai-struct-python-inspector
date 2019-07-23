import os
import sys

script_path = os.path.realpath(__file__)
tests_dir = os.path.dirname(script_path)
root_dir = os.path.dirname(tests_dir)
sys.path.insert(0, root_dir)


def test_inspector():
    from inspector import Inspector

    ksy_file = os.path.join(tests_dir, 'data/png.ksy')
    test_file = os.path.join(tests_dir, 'data/sample.png')

    Inspector(ksy_file, test_file, verbose=True)

    print('OK')


if __name__ == "__main__":
    test_inspector()
