import argparse
from typing import Dict, List, Optional
import os
import json


def parse_args(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default='input.json',
        help="input file to be changed",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default='input_new.json',
        help="input file changed",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args


if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    js_old = json.load(open(dict_args['input'], 'r'))
    type_map=['Ag', 'Al', 'As', 'Au', 'B', 'Bi', 'C', 'Ca', 'Cd', 'Cl', 'Co',
           'Cr', 'Cs', 'Cu', 'Fe', 'Ga', 'Ge', 'H', 'Hf', 'Hg', 'In', 'Ir',
           'K', 'Mg', 'Mn', 'Mo', 'N', 'Na', 'Nb', 'Ni', 'O', 'Os', 'P', 'Pb',
           'Pd', 'Pt', 'Rb', 'Re', 'Rh', 'Ru', 'S', 'Sb', 'Sc', 'Se', 'Si',
           'Sn', 'Sr', 'Ta', 'Tc', 'Te', 'Ti', 'Tl', 'V', 'W', 'Y', 'Zn',
           'Zr']
    js_old['model']['type_map'] = type_map
    js_old['model']['descriptor']['sel'] = [2]*len(type_map)
    with open(dict_args['output'], 'w') as ff:
        json.dump(js_old, ff, indent=1)
    print('put {} in type_map and sel done!'.format(type_map))








