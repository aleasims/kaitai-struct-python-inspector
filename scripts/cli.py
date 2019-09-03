import argparse
import sys

import kspyspector
from kspyspector.inspector import Inspector


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ksy_file', type=str,
                        help='path to .ksy file')
    parser.add_argument('bin_file', type=str,
                        help='path to binary file')
    parser.add_argument('-o', '--output', type=str, choices=['dot', 'trawl'],
                        help='serialize builded tree')
    parser.add_argument('-f', '--file', type=str,
                        help='output to file (stdout, if not set)')
    parser.add_argument('-v', '--verbose', action='store_true')    
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {}'.format(kspyspector.__version__))
    return parser.parse_args()


def main():
    args = parse_args()

    insp = Inspector(args.ksy_file, args.bin_file, args.verbose)

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
