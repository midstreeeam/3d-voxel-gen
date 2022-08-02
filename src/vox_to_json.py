import json
import numpy as np
from PIL import Image

from voxio.pyvox.parser import VoxParser
from helper import plot_3d


def vox2json(vox_path,palette_path,json_name):

    m = VoxParser(vox_path).parse()

    arr = np.zeros((31,31,31,4))
    '''
    arr[x,y,z]
    x+: close
    y+: right
    z+: up
    '''

    color = np.array(Image.open(palette_path))

    for i in m.models[0][1]:
        x=i.x
        y=i.y
        z=i.z
        c=i.c
        arr[x,y,z]=color[0,c-1]/255

    with open('data/json/'+json_name+'.json','w') as f:
        data = json.dumps(arr.tolist())
        f.write(data)
    
    print('transfer done')


def viz_json(json_name):
    
    with open('data/json/'+json_name+'.json','r') as f:
        arr = np.array(json.loads(f.read()))

    plot_3d(arr)


# vox2json('data/vox/cat/cat1-3.vox','data/palette/cat1.png','cat1-3')
# viz_json('cat1-3')