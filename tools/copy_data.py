import os
import shutil
from tqdm import tqdm
from IPython import embed
import argparse
from typing import Dict, List, Optional
import glob
import numpy as np
def parse_args(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        default='.',
        help="data path to explore",
    )
    parser.add_argument(
        "-p",
        "--out_path",
        type=str,
        default='',
        help="txt file to output",
    )
    parser.add_argument(
        "-f",
        "--frames_max",
        type=int,
        default=0,
        help="max frames",
    )
    parsed_args = parser.parse_args(args=args)
    return parsed_args
if __name__ == '__main__':
    args = parse_args()
    dict_args = vars(args)
    alist =[i.strip() for i in  open(dict_args['input_file'],'r').readlines()]
    fm = dict_args['frames_max']
    if fm == 0:
        for item in tqdm(alist):
            if 'data.iters' in item:
                name = item.split('/')[-3]+'_'+item.split('/')[-1]
            else:
            	name = item.split('/')[-1]
            shutil.copytree(item, os.path.join(dict_args['out_path'], name))
    else:
        for item in tqdm(alist):
            name = item.split('/')[-1]
            set_list = glob.glob(os.path.join(item, 'set.*'))
            part_ind = 0
            for set_ind in set_list:
                coord = np.load(os.path.join(set_ind, 'coord.npy'))
                box = np.load(os.path.join(set_ind, 'box.npy'))
                force = np.load(os.path.join(set_ind, 'force.npy'))
                energy = np.load(os.path.join(set_ind, 'energy.npy'))
                nframes = coord.shape[0]
                npart = nframes // fm
                if nframes % fm != 0:
                    npart += 1
                for i in range(npart):
                    name_par = name + '_part{}'.format(str(i + part_ind))
                    coord_par = coord[fm * i:fm * (i + 1)]
                    box_par = box[fm * i:fm * (i + 1)]
                    force_par = force[fm * i:fm * (i + 1)]
                    energy_par = energy[fm * i:fm * (i + 1)]
                    dst_path = os.path.join(dict_args['out_path'], name_par)
                    dst_set_path = os.path.join(dst_path, 'set.000')
                    os.mkdir(dst_path)
                    os.mkdir(dst_set_path)
                    shutil.copy(os.path.join(item, 'type.raw'), dst_path)
                    shutil.copy(os.path.join(item, 'type_map.raw'), dst_path)
                    np.save(os.path.join(dst_set_path, 'coord.npy'), coord_par)
                    np.save(os.path.join(dst_set_path, 'box.npy'), box_par)
                    np.save(os.path.join(dst_set_path, 'force.npy'), force_par)
                    np.save(os.path.join(dst_set_path, 'energy.npy'), energy_par)
                part_ind += npart


