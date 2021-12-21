import numpy as np
import os




def read_rgb(rgb_file_path, resolution:(int, int) = (160, 120)):
    (width, height) = resolution
    with open (rgb_file_path, 'rb') as f:
        data = f.read()
    data = [int(x) for x in data]
    npdata = np.array(data).astype(np.uint8)
    frames = int(npdata.shape[0] / (width * height * 3))
    npdata = npdata.reshape((3, height, 3, frames))
    return npdata