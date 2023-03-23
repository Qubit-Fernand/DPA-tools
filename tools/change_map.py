import dpdata
from IPython import embed
from tqdm import tqdm
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
        "-o",
        "--out_log",
        type=str,
        default='.',
        help="log file with failed cases",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    datafile = dict_args['path_file']
    data_sys = open(datafile, 'r')
    data_sys = [i.strip() for i in data_sys.readlines()]
    type_map = ['Li', 'P', 'S', 'Si', 'Ge', 'Sn']
    log = open(dict_args['out_log'], 'w')
    failed = []
    for single_system in tqdm(data_sys):
        try:
            temps = dpdata.LabeledSystem(single_system, fmt='deepmd/npy')
        except:
            print('not a system in{}'.format(single_system))
            continue
        try:
            temps.apply_type_map(type_map)
            temps.to_deepmd_npy(single_system)
        except:
            print(single_system)
            failed.append(single_system+'\n')
    log.writelines(failed)
    log.close()
