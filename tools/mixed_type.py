from IPython import embed
import numpy as np
import dpdata
import ase.io
import os
from tqdm import tqdm
import threading
import glob

type_map = ["Ag","Al","As","Au","B","Ba","Be","Bi","Br","C","Ca","Cd","Cl","Co",
            "Cr","Cs","Cu","F","Fe","Ga","Ge","H","Hf","Hg","I","In","Ir","K","Li","Mg",
            "Mn","Mo","N","Na","Nb","Ni","O","Os","P","Pb","Pd","Pt","Rb","Re","Rh","Ru",
            "S","Sb","Sc","Se","Si","Sn","Sr","Ta","Tc","Te","Ti","Tl","V","W","Y","Zn","Zr"]


ELEMENTS=['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr',
         'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag',
         'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
         'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np',
         'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr']

ELEMENTS = np.array(ELEMENTS)
ref_energy = True
data_dir = '/home/zhangduo/OC/s2ef_val_id/s2ef_val_id_uncompress'
output_dir_all = '/home/zhangduo/OC/processed/s2ef_val_id_ref'


# one thread
def process_list(file_list, thread_idx):
    output_dir = os.path.join(output_dir_all, str(thread_idx))
    try:
        os.mkdir(output_dir)
    except:
        pass
    nsys = {}  # 每个natoms的sys目前有几个
    num_sys = {}  # 每个natoms的sys目前排到第几个frame
    real_sys = {}  # 存放临时的每个natoms的sys
    failed_list = []
    natoms_list =[]
    skiped = []
    # # one file
    # data_path = '/home/zhangduo/OC/s2ef_train_2M/test_1/1.extxyz'
    for data_path in tqdm(file_list):
        name_path = os.path.join(data_dir, data_path.split('/')[-1].split('.')[0]+'.txt')
        f_data = ase.io.read(data_path, ":")
        f_name = [i.strip() for i in open(name_path, 'r').readlines()]
        for i, frames in enumerate(f_data):
            type_name = ELEMENTS[frames.get_atomic_numbers() - 1]
            natoms = type_name.size
            coord = frames.get_positions().reshape(natoms, 3)
            box = frames.get_cell().reshape(3, 3)
            energy = frames.get_potential_energy(apply_constraint=False)
            if ref_energy:
                energy -= float(f_name[i].split(',')[2])
            forces = frames.get_forces(apply_constraint=False).reshape(natoms, 3)
            # type_frame = [type_map.index(i) for i in type_name]
            temp_data = {'type_name': type_name,
                         'coord': coord,
                         'box': box,
                         'energy': energy,
                         'forces': forces}
            temp_sys = dpdata.LabeledSystem(temp_data, type_map=type_map, fmt='oc')
            temp_sys.convert_to_sel(type_map=type_map)
            if np.isnan(temp_sys.data['energies']).any():
                failed_list.append(name_path+':  '+f_name[i]+'\n')
                print('failed in ', name_path+':  '+f_name[i])
                continue
            natom = temp_sys.data['atom_types'].size
            if natom not in natoms_list:
                natoms_list.append(natom)
                natoms_list = sorted(natoms_list)
                os.mkdir(os.path.join(output_dir, str(natom)))
            if str(natom) not in nsys:
                nsys[str(natom)] = 0
            if str(natom) not in num_sys:
                num_sys[str(natom)] = 0
            num_sys[str(natom)] += 1

            if str(natom) not in real_sys or real_sys[str(natom)] == []:
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
        if num_sys[str(natom)] != 0:
            sys_path = os.path.join(output_dir, str(natom), 'sys.' + "%.6d" % nsys[str(natom)])
            real_sys[str(natom)].to_deepmd_sel(sys_path)
    ff = open('/home/zhangduo/OC/s2ef_train_2M/failed_cases_{}.txt'.format(thread_idx), 'w')
    ff.writelines(failed_list)
    ff.close()
    ff = open('/home/zhangduo/OC/s2ef_train_2M/natoms_{}.txt'.format(thread_idx), 'w')
    ff.writelines(str(natoms_list))
    ff.close()
    # ff = open('skip_{}.txt'.format(thread_idx), 'w')
    # ff.writelines(skiped)
    # ff.close()


# def process_list(pro_list):
#     natoms = []
#     nsys = {}  # 每个natoms的sys目前有几个
#     num_sys = {}  # 每个natoms的sys目前排到第几个frame
#     real_sys = {}  # 存放临时的每个natoms的sys
#     total_len = len(pro_list)
#     failed_list = []
#     skiped = []
#     for i in tqdm(range(total_len)):
#         item = pro_list[i]
#         temp = dpdata.LabeledSystem(item, fmt='deepmd/npy')
#         temp.convert_to_sel()
#         if np.isnan(temp.data['energies']).any():
#             failed_list.append(item+'\n')
#             print('failed in ', item)
#             continue
#         natom = temp.data['atom_types'].size
#         if natom not in natoms:
#             natoms.append(natom)
#             natoms = sorted(natoms)
#             os.mkdir(os.path.join(output_dir, str(natom)))
#         if str(natom) not in nsys:
#             nsys[str(natom)] = 0
#         if str(natom) not in num_sys:
#             num_sys[str(natom)] = 0
#         num_sys[str(natom)] += 1
#
#         if str(natom) not in real_sys or real_sys[str(natom)] == []:
#             real_sys[str(natom)] = temp
#         else:
#             real_sys[str(natom)].append(temp)
#
#         if num_sys[str(natom)] >= 200:
#             sys_path = os.path.join(output_dir, str(natom), 'sys.' + "%.6d" % nsys[str(natom)])
#             real_sys[str(natom)].to_deepmd_sel(sys_path)
#             nsys[str(natom)] += 1
#             real_sys[str(natom)] = []
#             num_sys[str(natom)] = 0
#     for natom in natoms:
#         if num_sys[str(natom)] != 0:
#             sys_path = os.path.join(output_dir, str(natom), 'sys.' + "%.6d" % nsys[str(natom)])
#             real_sys[str(natom)].to_deepmd_sel(sys_path)
#     ff = open('failed_cases.txt', 'w')
#     ff.writelines(failed_list)
#     ff.close()
#     ff = open('natoms.txt', 'w')
#     ff.writelines(str(natoms))
#     ff.close()
#     ff = open('skip.txt', 'w')
#     ff.writelines(skiped)
#     ff.close()
#
class myThread (threading.Thread):
    def __init__(self, threadID, pro_list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.pro_list = pro_list
    def run(self):
        process_list(self.pro_list, self.threadID)

thread_pool = []
f = [i.strip() for i in glob.glob(os.path.join(data_dir, "*.extxyz"))]
embed()
pro_len = len(f)
num_thread = 1
num_per_thread = int(pro_len/num_thread)
for i in range(num_thread):
    if i != num_thread-1:
        thread_pool.append(myThread(i, f[i*num_per_thread:(i+1)*num_per_thread]))
    else:
        thread_pool.append(myThread(i, f[i*num_per_thread:]))
    print(i, 'created!')

for thr in thread_pool:
    thr.start()

for thr in thread_pool:
    thr.join()
















