import json
import os
import subprocess

import yaml

from kspyspector import utils


class KsyError(Exception):
    pass


class Ksy:
    """Represent ksy file.

    Attrs:
        path - path to ksy file

    Methods to use:
        interpret()
        compile()

    After compilation, following attrs will be set:
        spec_name - id of the format specified in the ksy
        module - created module
        parser - created parser from module
    """

    def __init__(self, path):
        self.path = path

    def interpret(self):
        """Return loaded version of ksy."""

        return yaml.safe_load_all(open(self.path))

    def compile(self, outdir=None, clear=True):
        """Compile ksy with ksc.

        Args:
            outdir - path to dir, where to store created module
            clear - clear output directory at the end

        Created module can be saved or deleted at the end.

        Return parser class.
        """

        outdir = outdir if outdir is not None else utils.tmpdir()
        output = call_ksc(self.path, 'python', outdir=outdir, debug=True,
                          ksc_json_output=True, verbose=True)

        class_name, module_filename = self._parse_output(output)
        module_path = os.path.join(outdir, module_filename)
        self.module = utils.import_module(self.spec_name, module_path)

        self.parser = utils.get_class(self.module, class_name)

        if clear:
            if os.path.exists(self.module.__file__):
                os.remove(self.module.__file__)
            del outdir

        return self.parser

    def _parse_output(self, output):
        """Extract important fields from ksc output."""

        result = json.loads(output)[self.path]

        self.spec_name = result['firstSpecName']
        mod_params = result['output']['python'][self.spec_name]

        return (mod_params['topLevelName'],
                mod_params['files'].pop()['fileName'])


def call_ksc(ksy_path, target, outdir='.', debug=False,
             ksc_json_output=False, verbose=False):
    """Run kaitaistruct compiler in subprocess with params.

    Return the output of process.
    """

    cmd = ['ksc', '--target', target, '--outdir', outdir, ksy_path]
    if debug:
        cmd += ['--debug']
    if ksc_json_output:
        cmd += ['--ksc-json-output']

    if verbose:
        print(' '.join(cmd))

    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if err:
        raise KsyError(err.decode('utf-8'))

    if verbose:
        print(out)

    return out
