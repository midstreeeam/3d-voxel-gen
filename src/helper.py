from operator import methodcaller
import matplotlib.pylab as plt
import numpy as np
import random
from copy import deepcopy
import os

from voxio.pyvox.models import Vox

def plot_3d(arr):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    u = np.moveaxis(arr, (0, 1), (0, 1))
    m = ax.voxels((u[:, :, :, 3] > 0.1), facecolors=np.clip(u[:, :, :, :4], 0, 1))
    plt.show()
    plt.close()

def save_3d(arr,dpi=200):
    '''save figure under the folder 'img', with number as the name of the figure '''
    imgcount=len(os.listdir('img'))+1
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    u = np.moveaxis(arr, (0, 1), (0, 1))
    ax.voxels((u[:, :, :, 3] > 0.1), facecolors=np.clip(u[:, :, :, :4], 0, 1))
    plt.savefig("img/{}.jpg".format(imgcount),dpi=dpi,bbox_inches='tight',pad_inches=0)
    plt.close()


def single_color_mute(color,mute_range=5):
    [r,g,b,l]=color[0],color[1],color[2],color[3]
    if r>10 and r<240:
        r=r+random.randint(-mute_range,mute_range)
    if g>10 and g<245:
        g=g+random.randint(-mute_range,mute_range)
    if b>10 and b<245:
        b=b+random.randint(-mute_range,mute_range)

    ans=[r/255,g/255,b/255,l]

    return deepcopy(ans)

def model_to_list(model:Vox,palette_arr:np.ndarray,color_mute=False,single_color=None):

    arr = np.zeros((31,31,31,4))
    color = palette_arr

    for i in model.models[0][1]:
        x=i.x
        y=i.y
        z=i.z
        c=i.c

        if single_color is not None:
            arr[x,y,z]=single_color
        elif color_mute:
            arr[x,y,z]=single_color_mute(color[0,c-1])
        else:
            arr[x,y,z]=color[0,c-1]/255

    return arr
