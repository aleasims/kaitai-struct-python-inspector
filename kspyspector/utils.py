import importlib.util
import inspect
import os
import shutil
import time


class TmpDir(str):
    def __init__(self, path):
        super().__init__()
        os.makedirs(path, exist_ok=True)

    def __del__(self):
        if os.path.exists(self):
            shutil.rmtree(self)


def tmpdir(root='/tmp/kaitai/'):
    path = os.path.join(root, '{pid}_{time}'.format(
        pid=os.getpid(), time=int(time.time())))
    return TmpDir(path)


def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InspectionError(Exception):
    pass


def get_class(module, name):
    for objname, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and objname == name:
            return obj
    raise InspectionError('Parser class not found in compiled code.')
