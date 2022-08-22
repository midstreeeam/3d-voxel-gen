from filter import Filter
from helper import plot_3d
from vox_to_json import viz_vox
from voxio.pyvox.parser import VoxParser
from struct import unpack_from, calcsize

# arr=viz_vox('data/vox/cat/cat2.vox','data/palette/cat2-c3.png',color_mute=True)

# f=Filter('filter1')
# plot_3d(f.apply_to(arr,filter_effect='lighter',filter_color=[229/255,211/255,206/255,1]))

# viz_vox('data/vox/cat/cat1.vox','data/palette/cat1.png')
# viz_vox('data/vox/cat/cat2.vox','data/palette/cat2.png')
# viz_vox('data/vox/cat/cat3.vox','data/palette/cat3.png')

viz_vox('data/vox/cat/cat1.vox','data/palette/cat2-mod2.png')

# m = VoxParser('data/vox/cat/cat1.vox').parse()

# with open('data/vox/0.99/3x3x3.vox','rb') as f:
#     content = f.read()

# content = unpack_from('4si', content, 0)


# with open('test.txt','w') as f:
#     f.write(str(content))
