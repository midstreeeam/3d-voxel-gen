import imageio
import random
import os

def imgs2gif(imgPaths, saveName, duration=None, loop=0, fps=None):
    if fps:
        duration = 1 / fps
    images = [imageio.imread(str(img_path)) for img_path in imgPaths]
    imageio.mimsave(saveName, images, "gif", duration=duration, loop=loop)


p_lis = []
imgcount = len(os.listdir('img'))
for i in range(3,600,5):
  p_lis.append('./img/'+str(i)+'.jpg')

random.shuffle(p_lis)

imgs2gif(p_lis, "test.gif", 0)
