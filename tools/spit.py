import dpdata
import glob
from IPython import embed
from tqdm import tqdm

MgAlCu = open('./MgAlCu.txt', 'w')
MgAl = open('./MgAl.txt', 'w')
MgCu = open('./MgCu.txt', 'w')
AlCu = open('./AlCu.txt', 'w')
Mg = open('./Mg.txt', 'w')
Al = open('./Al.txt', 'w')
Cu = open('./Cu.txt', 'w')

MgAlCu_list = []
MgAl_list = []
MgCu_list = []
AlCu_list = []
Mg_list = []
Al_list = []
Cu_list = []

for single_system in tqdm(sorted(glob.glob('/opt/shared-data/data/AlMgCu/data/*'))+sorted(glob.glob('/opt/shared-data/data/AlMgCu/data.iters/*/*/*'))):
    try:
        temps = dpdata.LabeledSystem(single_system, fmt='deepmd/npy')
    except:
        print('not a system in{}'.format(single_system))
        continue
    temp_type = temps.get_atom_types()
    if 0 in temp_type and 1 in temp_type and 2 in temp_type:
        MgAlCu_list.append(single_system)
    elif 0 in temp_type and 1 in temp_type and 2 not in temp_type:
        MgAl_list.append(single_system)
    elif 0 in temp_type and 1 not in temp_type and 2 in temp_type:
        MgCu_list.append(single_system)
    elif 0 not in temp_type and 1 in temp_type and 2 in temp_type:
        AlCu_list.append(single_system)
    elif 0 in temp_type and 1 not in temp_type and 2 not in temp_type:
        Mg_list.append(single_system)
    elif 0 not in temp_type and 1 in temp_type and 2 not in temp_type:
        Al_list.append(single_system)
    elif 0 not in temp_type and 1 not in temp_type and 2 in temp_type:
        Cu_list.append(single_system)
    else:
        print('error in {}'.format(single_system))
MgAlCu.writelines(["{}\n".format(i) for i in MgAlCu_list])
MgAl.writelines(["{}\n".format(i) for i in MgAl_list])
MgCu.writelines(["{}\n".format(i) for i in MgCu_list])
AlCu.writelines(["{}\n".format(i) for i in AlCu_list])
Mg.writelines(["{}\n".format(i) for i in Mg_list])
Al.writelines(["{}\n".format(i) for i in Al_list])
Cu.writelines(["{}\n".format(i) for i in Cu_list])
MgAlCu.close()
MgAl.close()
MgCu.close()
AlCu.close()
Mg.close()
Al.close()
Cu.close()
embed()







