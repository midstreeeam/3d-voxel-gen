import math
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
import numpy as np
import matplotlib.pylab as plt
from pyvox.parser import VoxParser
import json
from tensorflow import pad
from tensorflow import cast, float32
from PIL import Image
import copy

p = 32
imgcount = len(os.listdir('img'))
print(imgcount)

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
    global imgcount
    imgcount+=1
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    #u = np.moveaxis(arr, (0, 1), (1, 2))
    u=arr
    m = ax.voxels((u[:, :, :, 3]), facecolors=np.clip(u[:, :, :, :4], 0, 1))
    # plt.savefig("img/{}.jpg".format(imgcount),dpi=900,bbox_inches='tight',pad_inches=0)
    plt.show()

# coloredlogs.install(level='DEBUG')


m = VoxParser('voxio/vox/cat3_head.vox').parse()

arr = np.zeros((16,16,16,4))

I = Image.open('voxio/vox/cat3.png')
color = np.array(I)


for i in m.models[0][1]:
    x=i.x
    y=i.y
    z=i.z
    c=i.c
    #arr[x,y,z]=single_color_mute(color[0,c-1])
    arr[x,y,z]=color[0,c-1]/255
    #arr[x,y,z][3]=0.5
    #arr[x,y,z]=[0,0,1,0.2]


# # arr[5, 5, 5] = [0,0,1,1]
# arr[7, 14, 14] = [1,0,0,1]
# arr[7, 14, 15] = [1,0,0,1]
# # arr[20, 20, 20] = [0,1,0,1]
# # arr[5, 5, 5] = [0,0,1,1]
# arr[0, 0, 0] = [0,1,1,1]

'''
arr[x,y,z]
x+: close
y+: right
z+: up
'''

targets = [arr]

pad_targets = [cast(pad_tgt(target_img), float32) for target_img in targets]
h, w, d = pad_targets[0].shape[:3]

seed = np.zeros([len(targets), h, w, d, 16], np.float32)
#seed[0, 8, 8, 8, 3:] = 1.0

# for cat1_head
# #head
# seed[0, 15, 15, 15, 3:] = 1.0
# seed[0, 16, 16, 16, 3:] = 1.0

# #ear
# seed[0, 15, 21, 22, 3:] = 1.0
# seed[0, 15, 22, 22, 3:] = 1.0
# #seed[0, 23, 23, 23, 3:] = 1.0

#for cat3_head
#head
seed[0, 15, 15, 15, 3:] = 1.0
seed[0, 15, 15, 16, 3:] = 1.0

#ear
seed[0, 14, 22, 21, 3:] = 1.0
seed[0, 14, 22, 22, 3:] = 1.0


# plot_3d(pad_targets[0])

# plot_3d(seed[0,:,:,:,:4])

with open('cat3_head.json','w') as f:
    data = json.dumps(arr.tolist())
    f.write(data)
