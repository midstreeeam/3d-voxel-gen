import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')

from pyvox.models import Vox
from pyvox.writer import VoxWriter


a = np.linalg.norm(np.mgrid[-5:5:10j, -5:5:10j, -5:5:10j], axis=0) < 4

vox = Vox.from_dense(a)

print(vox)

#VoxWriter('test.vox', vox).write()
