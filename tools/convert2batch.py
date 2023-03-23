import dpdata
import json
import os

import numpy as np
from IPython import embed
from tqdm import tqdm
import threading


output_dir = '/home/zhangduo/OQMD_processed/batch_sel_scaled/valid'


def process_list(pro_list):
    natoms = []
    nsys = {}  # 每个natoms的sys目前有几个
    num_sys = {}  # 每个natoms的sys目前排到第几个frame
    real_sys = {}  # 存放临时的每个natoms的sys
    total_len = len(pro_list)
    failed_list = []
    skiped = []
    for i in tqdm(range(total_len)):
        item = pro_list[i]
        temp = dpdata.LabeledSystem(item, fmt='deepmd/npy')
        temp.convert_to_sel()
        if np.isnan(temp.data['energies']).any():
            failed_list.append(item+'\n')
            print('failed in ', item)
            continue
        natom = temp.data['atom_types'].size
        if natom not in natoms:
            natoms.append(natom)
            natoms = sorted(natoms)
            os.mkdir(os.path.join(output_dir, str(natom)))
        if str(natom) not in nsys:
            nsys[str(natom)] = 0

        if str(natom) not in num_sys:
            num_sys[str(natom)] = 0
        num_sys[str(natom)] += 1

        if str(natom) not in real_sys or real_sys[str(natom)] == []:
            real_sys[str(natom)] = temp
        else:
            real_sys[str(natom)].append(temp)

        if num_sys[str(natom)] >= 200:
            sys_path = os.path.join(output_dir, str(natom), 'sys.' + "%.6d" % nsys[str(natom)])
            real_sys[str(natom)].to_deepmd_sel(sys_path)
            nsys[str(natom)] += 1
            real_sys[str(natom)] = []
            num_sys[str(natom)] = 0
    for natom in natoms:
        if num_sys[str(natom)] != 0:
            sys_path = os.path.join(output_dir, str(natom), 'sys.' + "%.6d" % nsys[str(natom)])
            real_sys[str(natom)].to_deepmd_sel(sys_path)

    ff = open('failed_cases.txt', 'w')
    ff.writelines(failed_list)
    ff.close()
    ff = open('natoms.txt', 'w')
    ff.writelines(str(natoms))
    ff.close()
    ff = open('skip.txt', 'w')
    ff.writelines(skiped)
    ff.close()


class myThread (threading.Thread):
    def __init__(self, threadID, pro_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.pro_list =pro_list
    def run(self):
        process_list(self.pro_list)

thread_pool = []
f = [i.strip() for i in open('/home/zhangduo/OQMD_processed/no_failed/valid.txt', 'r').readlines()]
pro_len = len(f)
num_thread = 1
num_per_thread = int(pro_len/num_thread)
for i in range(num_thread):
    embed()
    if i != num_thread-1:
        thread_pool.append(myThread(i, f[i*num_per_thread:(i+1)*num_per_thread]))
    else:
        thread_pool.append(myThread(i, f[i*num_per_thread:]))
    print(i, 'created!')

for thr in thread_pool:
    thr.start()

for thr in thread_pool:
    thr.join()



