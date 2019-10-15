"""
    Example usage:
kspyspector tests/data/sample.ksy tests/data/sample.bin
"""

import argparse
import sys

import kspyspector
from kspyspector.inspector import Inspector


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {}'.format(kspyspector.__version__))

    input_params = parser.add_argument_group('input')
    input_params.add_argument('ksy_file', type=str,
                              help='path to .ksy file')
    input_params.add_argument('bin_file', type=str,
                              help='path to binary file')

    build_params = parser.add_argument_group('build flags')
    build_params.add_argument('-e', '--empty_ommit', action='store_true',
                              help='do NOT include empty fields in result')

    output_params = parser.add_argument_group('output')
    output_params.add_argument('-o', '--output', type=str,
                               choices=['dot', 'trawl'],
                               help='serialize builded tree')
    output_params.add_argument('-f', '--file', type=str,
                               help='output to file (to stdout, if not set)')
    return parser.parse_args()


def main():
    args = parse_args()

    insp = Inspector(args.ksy_file, args.bin_file, args.empty_ommit,
                     args.verbose)

    if args.output is not None:
        out_file = sys.stdout if args.file is None else open(args.file, 'w')
        if args.output == 'dot':
            print(insp.to_dot(), file=out_file)
        elif args.output == 'trawl':
            print(insp.to_trawl(), file=out_file)
        else:
            out_file.close()
            raise ValueError('Unknown output format')
        out_file.close()
