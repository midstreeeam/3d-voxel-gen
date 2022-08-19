import imageio
import random
import os

def imgs2gif(imgPaths, saveName, duration=None, loop=0, fps=None):
    if fps:
        duration = 1 / fps
    images = [imageio.imread(str(img_path)) for img_path in imgPaths]
    imageio.mimsave(saveName, images, "gif", duration=duration, loop=loop)


p_lis = []
imgcount = len(os.listdir('img/color_mu_220615/'))
for i in range(3,imgcount,7):
  p_lis.append('./img/color_mu_220615/'+str(i)+'.jpg')

random.shuffle(p_lis)

imgs2gif(p_lis, "test.gif", 0)
