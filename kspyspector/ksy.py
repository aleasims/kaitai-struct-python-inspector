import os
import time
import subprocess
import yaml
import importlib.util
import inspect
import shutil


class CompilationError(Exception):
    pass


class create_tmp:
    """Context manager for creating and cleaning tmp dir."""
    def __enter__(self):
        self.path = '/tmp/kaitai_{}'.format(int(time.time()))
        os.mkdir(self.path)
        return self.path

    def __exit__(self, exc_type, exc_value, exc_traceback):
        shutil.rmtree(self.path)


def get_class_name(path):
    spec = yaml.load(open(path), Loader=yaml.FullLoader)
    return spec['meta']['id']


def import_compiled(tmp, name):
    name = name.lower()
    filename = os.path.join(tmp, name + '.py')
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def find_parser_class(module, name):
    for objname, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and objname.lower() == name:
            return obj
    raise ImportError('Parser class not found in compiled code.')


def compile(path, verbose=False):
    with create_tmp() as tmp:
        cmd = 'ksc --debug --target python --outdir {output} {file}'.format(
            file=path, output=tmp)
        if verbose:
            print(cmd)

        proc = subprocess.Popen(cmd.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if out or err:
            print('Something went wrong during compilation!')
            raise CompilationError(out.decode('utf-8'))

        name = get_class_name(path)
        module = import_compiled(tmp, name)
        Parser = find_parser_class(module, name)

    return Parser
