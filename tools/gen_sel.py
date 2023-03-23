import argparse
from typing import Dict, List, Optional
import os
from IPython import embed

def parse_args(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-n",
        "--num_of_types",
        type=int,
        default=1,
        help="--num of types",
    )
    parser.add_argument(
        "-e",
        "--each_sel",
        type=int,
        default=1,
        help="--each sel",
    )
    parser.add_argument(
        "-o",
        "--out_file",
        type=str,
        default='',
        help="txt file to output",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    output = open(dict_args['out_file'], 'w')
    num_of_types = dict_args['num_of_types']
    each_sel = dict_args['each_sel']
    out_list = [each_sel for i in range(num_of_types)]
    output.writelines(str(out_list))
    output.close()
