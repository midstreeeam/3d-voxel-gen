import matplotlib.pylab as plt
import numpy as np

def plot_3d(arr):
    global imgcount
    imgcount+=1
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    u = np.moveaxis(arr, (0, 1), (0, 1))
    ax.voxels((u[:, :, :, 3]), facecolors=np.clip(u[:, :, :, :4], 0, 1))
    plt.show()