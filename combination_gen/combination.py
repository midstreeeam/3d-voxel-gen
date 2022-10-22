import numpy as np
from PIL import Image
from copy import deepcopy
from filter import Filter

from PyVox.pyvox.voxio import *

from config import CAT_PATH, FILTER_PATH,PALETTE_PATH

class Cat():
    
    def __init__(self,name,palette_name='cat2') -> None:

        vox_path=CAT_PATH+name+'.vox'
        
        vox_path0=vox_path[:-4]+'-0'+vox_path[-4:]
        vox_path1=vox_path[:-4]+'-1'+vox_path[-4:]
        vox_path2=vox_path[:-4]+'-2'+vox_path[-4:]
        vox_path3=vox_path[:-4]+'-3'+vox_path[-4:]
        vox_path4=vox_path[:-4]+'-4'+vox_path[-4:]

        self.vox_path=[vox_path0,vox_path1,vox_path2,vox_path3,vox_path4]
        self.palette_path=PALETTE_PATH+palette_name+'.png'
        print(self.palette_path)

    pass


def vox_to_list(pet:Cat,vox_index,filter:Filter=None):
    vox_path=pet.vox_path[vox_index]
    palette_path=pet.palette_path
    m=get_vox(vox_path)

    I = Image.open(palette_path)
    color = np.array(I)[0]
    m.palettes.append(color)
    arr=m.to_list(palette_index=-1)
    filter_color=color[254]/255

    if filter is not None:
        # filter.apply_to(arr,filter_color=filter_color)
        filter.apply_to(arr)

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


def read_files(filter=None,palette_name='cat2-c3'):

    cat1=Cat('cat1',palette_name)
    cat2=Cat('cat2',palette_name)
    cat3=Cat('cat3',palette_name)
    cats=[cat1,cat2,cat3]

    arr=np.zeros((len(cats),5,31,31,31,4)) # examle: [cat1,tail,x,y,z,color]
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

    f=Filter('edge')
    pal_path='data/palette/light.png'
    arr=read_files(f,palette_name='light')

    hy=comb_1(arr)
    print('comb_1 hybrid_done')
    print(hy.shape)

    for i in hy:
        plot_3d(i)

    # hy=comb_2(arr)
    # print('comb_2 hybrid_done')
    # print(hy.shape)

    # for i in hy:
    #     save_vox(i,pal_path)
    #     save_3d(i)

run_combination()

# f=read_filter()
# arr=read_files(f)
# tails=arr[:,0,:,:,:,:]
# bodies=arr[:,1,:,:,:,:]
# limbs=arr[:,2,:,:,:,:]
# heads=arr[:,3,:,:,:,:]
# earsis=arr[:,4,:,:,:,:]