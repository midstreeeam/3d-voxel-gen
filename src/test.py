import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
from pyvox.parser import VoxParser

m = VoxParser('voxio/vox/cat_color_mod/cat1/divided/cat1-2.vox').parse()
print(m)
