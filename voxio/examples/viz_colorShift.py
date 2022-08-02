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
    plt.savefig("img/{}.jpg".format(imgcount),dpi=900,bbox_inches='tight',pad_inches=0)
    # plt.show()

# coloredlogs.install(level='DEBUG')

def single_color_mute(color):
    [r,g,b,l]=color[0],color[1],color[2],color[3]
    if r>10 and r<240:
        r=r+random.randint(-7,7)
    if g>10 and g<245:
        g=g+random.randint(-7,7)
    if b>10 and b<245:
        b=b+random.randint(-7,7)

    ans=[r/255,g/255,b/255,l]

    return copy.deepcopy(ans)

def color_lbg_mute(v:int):

    choose=random.random()
    if v>40 and v<215:
        if choose<0.5:
            v=v+random.randint(9,22)
        else:
            v=v-random.randint(9,22)
    elif v<40 and v>15:
        if choose<0.5:
            v=v+random.randint(9,22)
    elif v<240 and v>215:
        if choose<0.5:
            v=v-random.randint(9,22)

    return v

def color_mute(color:np.array):

    for i in range(255):
        [r,g,b]=color[0][i][0],color[0][i][1],color[0][i][2]

        color[0][i][0]=color_lbg_mute(color[0][i][0])
        color[0][i][1]=color_lbg_mute(color[0][i][1])
        color[0][i][2]=color_lbg_mute(color[0][i][2])
    
    return color


m = VoxParser('voxio/vox/cat1.vox').parse()

arr = np.zeros((31,31,31,4))

I = Image.open('voxio/vox/cat1.png')
color = np.array(I)


for i in range(5):
    print(color[0][i])
print()

for t in range(10):
    I = Image.open('voxio/vox/cat1.png')
    color = np.array(I)
    for j in range(3):

        color=color_mute(color)

        for i in range(5):
            print(color[0][i])
        print()

        blue=[0,0,1,1]

        for i in m.models[0][1]:
            x=i.x
            y=i.y
            z=i.z
            c=i.c
            arr[x,y,z]=single_color_mute(color[0,c-1])
            #arr[x,y,z]=color[0,c-1]/255
            #arr[x,y,z]=blue

        targets = [np.array(x) for x in [arr]]

        pad_targets = [cast(pad_tgt(target_img), float32) for target_img in targets]
        h, w, d = pad_targets[0].shape[:3]

        # seed = np.zeros([len(targets), h, w, d, 16], np.float32)

        # seed[0, h//2-12, w//2+12, d//2-6, 3:] = 1.0

        plot_3d(pad_targets[0])

# plot_3d(seed[0,:,:,:,:4])

# with open('tail.json','w') as f:
#     data = json.dumps(arr.tolist())
#     f.write(data)
