import matplotlib.pylab as plt
import numpy as np
import random
from copy import deepcopy
import os

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
    ax.voxels((arr[:, :, :, 3]), facecolors=np.clip(arr[:, :, :, :4], 0, 1))
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
