import argparse
from typing import Dict, List, Optional
import os
import glob
import dpdata
from tqdm import tqdm
from IPython import embed
import random
import numpy as np
type_map = ["Ag","Al","As","Au","B","Ba","Be","Bi","Br","C","Ca","Cd","Cl","Co",
            "Cr","Cs","Cu","F","Fe","Ga","Ge","H","Hf","Hg","I","In","Ir","K","Li","Mg",
            "Mn","Mo","N","Na","Nb","Ni","O","Os","P","Pb","Pd","Pt","Rb","Re","Rh","Ru",
            "S","Sb","Sc","Se","Si","Sn","Sr","Ta","Tc","Te","Ti","Tl","V","W","Y","Zn","Zr"]

def parse_args(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i",
        "--data_file",
        type=str,
        default='.',
        help="input data path file",
    )
    parser.add_argument(
        "-p",
        "--out_path",
        type=str,
        default='',
        help="out path to save",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    file_list = [i.strip() for i in open(dict_args['data_file'], 'r').readlines()]
    # random.shuffle(file_list)
    # output = open('shuffled_list.txt', 'w')
    # output.writelines(["{}\n".format(i) for i in file_list])
    # output.close()
    output_dir = dict_args['out_path']
    try:
        os.mkdir(output_dir)
    except:
        pass
    nsys = {}  # 每个natoms的sys目前有几个
    num_sys = {}  # 每个natoms的sys目前排到第几个frame
    real_sys = {}  # 存放临时的每个natoms的sys
    failed_list = []
    natoms_list =[]
    for sys in tqdm(file_list):
        temp_sys = dpdata.LabeledSystem(sys, fmt='deepmd/npy')
        natom = temp_sys.get_natoms()
        temp_sys.convert_to_sel(type_map=type_map)
        if np.isnan(temp_sys.data['energies']).any():
            failed_list.append(sys + '\n')
            print('failed in : ', sys)
            continue
        if natom not in natoms_list:
            natoms_list.append(natom)
            natoms_list = sorted(natoms_list)
            os.mkdir(os.path.join(output_dir, str(natom)))
        if str(natom) not in nsys:
            nsys[str(natom)] = 0
        if str(natom) not in num_sys:
            num_sys[str(natom)] = 0
        num_sys[str(natom)] += temp_sys.get_nframes()

        if str(natom) not in real_sys or real_sys[str(natom)] == []:  #  [] 代表空
            real_sys[str(natom)] = temp_sys
        else:
            real_sys[str(natom)].append(temp_sys)
        if num_sys[str(natom)] >= 200:
            sys_path = os.path.join(output_dir, str(natom), 'sys.' + "%.6d" % nsys[str(natom)])
            real_sys[str(natom)].to_deepmd_sel(sys_path)
            nsys[str(natom)] += 1
            real_sys[str(natom)] = []
            num_sys[str(natom)] = 0
    for natom in natoms_list:
        if num_sys[str(natom)] > 0:
            sys_path = os.path.join(output_dir, str(natom), 'sys.' + "%.6d" % nsys[str(natom)])
            real_sys[str(natom)].to_deepmd_sel(sys_path)
    ff = open('failed_cases.txt', 'w')
    ff.writelines(failed_list)
    ff.close()
    ff = open('natoms.txt', 'w')
    ff.writelines(str(natoms_list))
    ff.close()


