import random
import os

import numpy as np
import matplotlib.pylab as plt
from PIL import Image
from copy import deepcopy

from matplotlib.pyplot import plot
from voxio.pyvox.models import Vox
from voxio.pyvox.parser import VoxParser



imgcount = len(os.listdir('img'))
print(imgcount)

def save_3d(arr):
    global imgcount
    imgcount+=1
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.voxels((arr[:, :, :, 3]), facecolors=np.clip(arr[:, :, :, :4], 0, 1))
    plt.savefig("img/{}.jpg".format(imgcount),dpi=200,bbox_inches='tight',pad_inches=0)
    plt.close()


def single_color_mute(color):
    [r,g,b,l]=color[0],color[1],color[2],color[3]
    if r>10 and r<240:
        r=r+random.randint(-6,6)
    if g>10 and g<245:
        g=g+random.randint(-6,6)
    if b>10 and b<245:
        b=b+random.randint(-6,6)

    ans=[r/255,g/255,b/255,l]

    return deepcopy(ans)


class pet():
    
    def __init__(self,name,vox_path) -> None:
        # self.img_path=vox_path+'/'+name+'.png'
        self.img_path='voxio/vox/cat_color_mod/cat2/cat2-c2.png'
        vox_path=vox_path+'/divided/'+name+'.vox'
        
        vox_path0=vox_path[:-4]+'-0'+vox_path[-4:]
        vox_path1=vox_path[:-4]+'-1'+vox_path[-4:]
        vox_path2=vox_path[:-4]+'-2'+vox_path[-4:]
        vox_path3=vox_path[:-4]+'-3'+vox_path[-4:]
        vox_path4=vox_path[:-4]+'-4'+vox_path[-4:]
        self.vox_path=[vox_path0,vox_path1,vox_path2,vox_path3,vox_path4]

    pass
    

def plot_3d(arr):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    u = np.moveaxis(arr, (0, 1), (0, 1))
    m = ax.voxels((u[:, :, :, 3] > 0.1), 
                  facecolors=np.clip(u[:, :, :, :4], 0, 1))
    plt.show()


def color_normalize_index(m:Vox):
    return 0
    c_min=255
    for i in m.models[0][1]:
        if i.c<c_min:
            c_min=i.c
    return c_min

def read_filter():
    path='voxio/vox/filter/filter1.vox'
    m = VoxParser(path).parse()
    color=[0,0,1,1]
    arr = np.zeros((31,31,31,4))
    for i in m.models[0][1]:
        x=i.x
        y=i.y
        z=i.z
        arr[x,y,z]=color
    return arr


def vox_to_list(pet:pet,vox_index,filter=None):
    vox_path=pet.vox_path[vox_index]
    img_path=pet.img_path
    m = VoxParser(vox_path).parse()
    print(vox_path)
    arr = np.zeros((31,31,31,4))

    I = Image.open(img_path)
    color = np.array(I)
    color_index=color_normalize_index(m)

    for i in m.models[0][1]:
        x=i.x
        y=i.y
        z=i.z
        c=i.c-color_index
        # arr[x,y,z]=color[0,c-1]/255
        arr[x,y,z]=single_color_mute(color[0,c-1])
        if filter is not None:
            if filter[x,y,z,3]==1:
                arr[x,y,z]=color[0,34]/255
        new_color=arr[x,y,z]/0.9
        arr[x,y,z]=[new_color[0],new_color[1],new_color[2],1]

    return arr


def stack_two(arr1,arr2):
    '''stack arr2 on top of arr1'''
    arr=deepcopy(arr1)
    for x,y in np.ndenumerate(arr1[:,:,:,0]):
        if (arr1[x]==0).all():
            arr[x]=arr2[x]
    return arr


def hybrid(part1_list,part2_list):
    hylist=[]
    for i in range(len(part1_list)):
        for j in range(len(part2_list)):
            hylist.append(clean_limb_body_gap(stack_two(part1_list[i],part2_list[j])))
    return np.array(hylist)

def move_to_bottom(x:np.ndarray,col):
    new_column_order = [col, *range(col), *range(col+1,x.shape[1])]
    return x[:,:,new_column_order]

def clean_limb_body_gap(arr:np.ndarray):
    new_arr=deepcopy(arr)
    for i in range(int(arr.shape[2]/3)):
        if (arr[:,:,i]==0).all():
            new_arr=move_to_bottom(new_arr,i)

    return new_arr


def read_files(filter=None):

    cat1=pet('cat1','voxio/vox/cat_color_mod/cat1')
    cat2=pet('cat2','voxio/vox/cat_color_mod/cat2')
    cat3=pet('cat3','voxio/vox/cat_color_mod/cat3')
    cats=[cat1,cat2,cat3]

    arr=np.zeros((len(cats),5,31,31,31,4))
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i][j]=vox_to_list(cats[i],j,filter)

    return arr

def comb_1(arr:np.ndarray):
    '''combination for fat & medium, earsis are exceptions'''

    tails=arr[:,0,:,:,:,:] #tails[0] fat, tails[1] mid, tails[2] thin
    tails = tails[:2]
    bodies=arr[:,1,:,:,:,:]
    bodies = bodies[:2]
    limbs=arr[:,2,:,:,:,:]
    limbs = limbs[:2]
    heads=arr[:,3,:,:,:,:]
    heads = heads[:2]
    earsis=arr[:,4,:,:,:,:]
    
    hy1=hybrid(limbs,bodies)
    hy2=hybrid(tails,earsis)
    hy3=hybrid(hy1,hy2)
    hy4=hybrid(hy3,heads)

    return hy4

def comb_2(arr:np.ndarray):
    '''combination for medium & thin, tails and earsis are exceptions'''

    tails=arr[:,0,:,:,:,:] #tails[0] fat, tails[1] mid, tails[2] thin
    bodies=arr[:,1,:,:,:,:]
    bodies = bodies[1:]
    limbs=arr[:,2,:,:,:,:]
    limbs = limbs[1:]
    heads=arr[:,3,:,:,:,:]
    heads = heads[1:]
    earsis=arr[:,4,:,:,:,:]
    
    hy1=hybrid(limbs,bodies)
    hy2=hybrid(tails,earsis)
    hy3=hybrid(hy1,hy2)
    hy4=hybrid(hy3,heads)

    return hy4

def run_combination():

    f=read_filter()

    arr=read_files(f)

    '''
    0: tail
    1: body
    2: limbs
    3: head
    4: ears
    '''

    tails=arr[:,0,:,:,:,:]
    bodies=arr[:,1,:,:,:,:]
    limbs=arr[:,2,:,:,:,:]
    heads=arr[:,3,:,:,:,:]
    earsis=arr[:,4,:,:,:,:]


    # hy=comb_1(arr)
    # print('comb_1 hybrid_done')
    # print(hy.shape)

    # for i in hy:
    #     save_3d(i)

    hy=comb_2(arr)
    print('comb_2 hybrid_done')
    print(hy.shape)

    for i in hy:
        save_3d(i)

# run_combination()

# t=stack_two(arr[0][2],arr[2][1])
# t=clean_limb_body_gap(t)

# plot_3d(arr[1][3])
# plot_3d(arr[1][2])

arr= read_filter()
plot_3d(arr)
