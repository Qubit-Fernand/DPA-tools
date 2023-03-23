from tqdm import tqdm
import os
import shutil
import argparse
from typing import Dict, List, Optional
def parse_args(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i",
        "--path_file",
        type=str,
        default='.',
        help="path file to explore",
    )
    parser.add_argument(
        "-f",
        "--copy_file",
        type=str,
        default='.',
        help="file to copy",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    datafile = dict_args['path_file']
    data_sys = open(datafile, 'r')
    data_sys = [i.strip() for i in data_sys.readlines()]
    cp_file = dict_args['copy_file']
    for single_system in tqdm(data_sys):
        shutil.copyfile(cp_file, os.path.join(single_system, 'type_map.raw'))    
