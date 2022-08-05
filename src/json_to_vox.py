import json

import numpy as np

from voxio.pyvox.models import Vox
from voxio.pyvox.writer import VoxWriter

def json2vox(json_path,output_path):
    with open(json_path,'r') as f:
        data=json.loads(f.read())
    a=np.array(data)

    # cut if the size is not 31x31x31
    arr=a[:31,:31,:31,3]
    bool_arr=np.zeros(arr.shape,dtype=bool)

    # nested 'for' need to be improved
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            for z in range(arr.shape[2]):
                if abs(arr[x,y,z])<0.1:
                    bool_arr[x,y,z]=False
                else:
                    bool_arr[x,y,z]=True


    vox = Vox.from_dense(bool_arr)
    VoxWriter(output_path, vox).write()

json2vox('data/json/filter_rand70.json','data/vox/filter/filter_rand70.vox')