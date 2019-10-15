import importlib.util
import inspect
import json
import os
import shutil
import subprocess
import time

import yaml


class KsyError(Exception):
    pass


class TmpDir:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        os.makedirs(self.path, exist_ok=True)
        return self.path

    def __exit__(self, exc_type, exc_value, exc_traceback):
        shutil.rmtree(self.path)


def create_tmp():
    return TmpDir('/tmp/kaitai/{pid}_{time}'.format(
        pid=os.getpid(), time=int(time.time())))


def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compile_ksy(path, tmp, verbose=False):
    cmd = ['ksc',
           '--ksc-json-output',
           '--debug',
           '--target', 'python',
           '--outdir', tmp,
           path]
    if verbose:
        print(' '.join(cmd))

    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if err:
        print('Something went wrong during compilation!')
        raise KsyError(err.decode('utf-8'))
    return out


def parse_result(result, ksy_path, module_dir):
    result = json.loads(result)[ksy_path]
    target_lang = 'python'

    module_name = result['firstSpecName']
    module_spec = result['output'][target_lang][module_name]
    module_filename = module_spec['files'].pop()['fileName']
    module_path = os.path.join(module_dir, module_filename)

    class_name = module_spec['topLevelName']

    return module_name, module_path, class_name


def get_class(module, name):
    for objname, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and objname == name:
            return obj
    raise ImportError('Parser class not found in compiled code.')


def compile(path, verbose=False):
    with create_tmp() as tmp:
        result = compile_ksy(path, tmp, verbose)
        module_name, module_path, class_name = parse_result(result, path, tmp)
        module = import_module(module_name, module_path)
        Parser = get_class(module, class_name)
    return Parser
