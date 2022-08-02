from tensorflow import pad
from tensorflow import cast

def pad_tgt(p,tgt):
# tgt -- target model, stored in numpy array
    px = (p - tgt.shape[0]) // 2
    py = (p - tgt.shape[1]) // 2
    pz = (p - tgt.shape[2]) // 2
    return pad(tgt, [
        (px, px + (p - tgt.shape[0] - 2 * px)), 
        (py, py + (p - tgt.shape[1] - 2 * py)), 
        (pz, pz + (p - tgt.shape[2] - 2 * pz)), (0, 0)])