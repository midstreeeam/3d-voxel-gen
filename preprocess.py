import math
import sys
import os
import coloredlogs
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
import numpy as np
import matplotlib.pylab as plt
from voxio.pyvox.parser import VoxParser
import json
from tensorflow import pad
from tensorflow import cast, float32


p = 32

def pad_tgt(tgt):
  # tgt -- target model, stored in numpy array
    px = (p - tgt.shape[0]) // 2
    py = (p - tgt.shape[1]) // 2
    pz = (p - tgt.shape[2]) // 2
    return pad(tgt, [
        (px, px + (p - tgt.shape[0] - 2 * px)), 
        (py, py + (p - tgt.shape[1] - 2 * py)), 
        (pz, pz + (p - tgt.shape[2] - 2 * pz)), (0, 0)])


def plot_3d(arr):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    #u = np.moveaxis(arr, (0, 1), (1, 2))
    u=arr
    m = ax.voxels((u[:, :, :, 3]), facecolors=np.clip(u[:, :, :, :4], 0, 1))
    plt.show()

# coloredlogs.install(level='DEBUG')



# input the file name that you want to parse
n = VoxParser().parse()

arr = np.zeros((16,16,16,4))
arr2 = np.zeros((20,20,20,4))
color = [0,0,1,1]

# for i in m.models[0][1]:
#     x=i.x
#     y=i.y
#     z=i.z
#     c=i.c
#     arr[x,y,z]=color

for i in n.models[0][1]:
    x=i.x
    y=i.y
    z=i.z
    c=i.c
    arr2[x,y,z]=color

targets = [np.array(x) for x in [arr2]]
plot_3d(targets[0])
pad_targets = [cast(pad_tgt(target_img), float32) for target_img in targets]

# h, w, d = pad_targets[0].shape[:3]
# seed = np.zeros([len(targets), h, w, d, 16], np.float32)
# seed[0, h//2, w//2 , d//2, 3:] = 1.0
# plot_3d(seed[0,:,:,:,:4])

with open('output.json','w') as f:
    data = json.dumps(arr2.tolist())
    f.write(data)