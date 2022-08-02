import json
import matplotlib.pyplot as plt
import numpy as np

def plot_3d(arr):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    u = np.moveaxis(arr, (0, 1), (0, 1))
    m = ax.voxels((u[:, :, :, 3] > 0.1), 
                  facecolors=np.clip(u[:, :, :, :4], 0, 1))
    plt.show()


with open('hy_cat13_head_75.json','r') as f:
    cat3_data = json.loads(f.read())
cat = np.array(cat3_data)

# seed=np.zeros([4, 32, 32, 32, 16])
# seed[0, 15, 15, 14, 3:] = 1.0
# seed[0, 15, 15, 15, 3:] = 1.0
# seed[0, 15, 14, 14, 3:] = 1.0
# seed[0, 15, 13, 14, 3:] = 1.0
# seed[0, 15, 13, 15, 3:] = 1.0
# seed[0, 15, 15, 16, 3:] = 1.0
# seed[0, 15, 14, 16, 3:] = 1.0
# seed[0, 15, 13, 16, 3:] = 1.0


# seed[1, 13, 14, 15, 3:] = 1.0
# seed[1, 14, 14, 15, 3:] = 1.0
# seed[1, 15, 14, 15, 3:] = 1.0
# seed[1, 16, 14, 15, 3:] = 1.0
# seed[1, 17, 14, 15, 3:] = 1.0

plot_3d(cat)