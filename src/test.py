from filter import Filter
from helper import plot_3d
from vox_to_json import viz_vox

arr=viz_vox('data/vox/cat/cat2.vox','data/palette/cat2.png')
f=Filter('filter_rand70')
plot_3d(f.apply_to(arr,filter_effect='lighter'))