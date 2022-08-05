import numpy as np

from voxio.pyvox.parser import VoxParser
from helper import model_to_list

from config import CAT_PATH, FILTER_PATH,PALETTE_PATH

class Filter():

    def __init__(self,filter_name) -> None:
        self.filter_color=np.array([0,0,1,1])
        self.filter_arr=self._read_filter(filter_name)
        pass

    def _read_filter(self,name):
        path=FILTER_PATH+name+'.vox'
        m = VoxParser(path).parse()
        return model_to_list(m,[],color_mute=False,single_color=self.filter_color)
        

    def apply_to(self,model_arr:np.ndarray,filter_effect='lighter',filter_color=None):

        # need to be improved
        for x in range(model_arr.shape[0]):
            for y in range(model_arr.shape[1]):
                for z in range(model_arr.shape[2]):

                    if self.filter_arr[x,y,z,3]==1 and abs(model_arr[x,y,z,3])>0.01:
                        # filter condition
                        if filter_color is not None:
                            model_arr[x,y,z]=filter_color
                        elif filter_effect=='lighter':
                            new_color=model_arr[x,y,z]/0.87
                            model_arr[x,y,z]=[new_color[0],new_color[1],new_color[2],1]
                        elif filter_effect=='darker':
                            new_color=model_arr[x,y,z]/1.1
                            model_arr[x,y,z]=[new_color[0],new_color[1],new_color[2],1]

        return model_arr