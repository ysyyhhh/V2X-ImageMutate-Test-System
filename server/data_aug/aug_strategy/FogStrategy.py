import math
from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from pkg_resources import resource_filename

from data_aug.tools.file_tools import get_all_camera_ph
from .ops import plasma_fractal

import random



# 阴影扩增
def fog_aug(task_obj, config_obj, target_dir):
    print('--------------------------------------0')
    # 是否分别对不同车辆数据进行扩增
    separate_flag = config_obj.separate_flag

    file_list = get_all_camera_ph(target_dir, separate_flag)

    default_flag = config_obj.default_flag
    aug_para = config_obj.aug_para

    fog = Fog()


    for file in file_list:
        # 使用默认参数
        if (default_flag):
            img = Image.open(file)
            img = fog(img, mag=0, prob=1)
            # 保存输出图像
            img.save(file)
        else:
            img = Image.open(file)
            img = fog(img, mag=aug_para, prob=1)
            # 保存输出图像
            img.save(file)

class Fog:
    def __init__(self, rng=None):
        self.rng = np.random.default_rng() if rng is None else rng

    def __call__(self, img, mag=-1, prob=1.):
        if self.rng.uniform(0, 1) > prob:
            return img

        w, h = img.size
        c = [(1.5, 2), (3.5, 2.6), (6.5, 5.7)]
        if mag < 0 or mag >= len(c):
            index = self.rng.integers(0, len(c))
        else:
            index = mag
        c = c[index]

        n_channels = len(img.getbands())
        isgray = n_channels == 1

        img = np.asarray(img) / 255.
        max_val = img.max()
        # Make sure fog image is at least twice the size of the input image
        max_size = 2 ** math.ceil(math.log2(max(w, h)) + 1)
        fog = c[0] * plasma_fractal(mapsize=max_size, wibbledecay=c[1], rng=self.rng)[:h, :w][..., np.newaxis]
        # x += c[0] * plasma_fractal(wibbledecay=c[1])[:224, :224][..., np.newaxis]
        # return np.clip(x * max_val / (max_val + c[0]), 0, 1) * 255
        if isgray:
            fog = np.squeeze(fog)
        else:
            fog = np.repeat(fog, 3, axis=2)

        img += fog
        img = np.clip(img * max_val / (max_val + c[0]), 0, 1) * 255
        return Image.fromarray(img.astype(np.uint8))



def random_half_list(lst):
    half_length = len(lst) // 2
    random.shuffle(lst)
    new_lst = lst[:half_length]
    return new_lst



if __name__ == '__main__':
    img = Image.open('1.png')
    fog = Fog()

    img = fog(img, mag=2, prob=1)
    # 保存输出图像
    img.save('1_fog.png')

    # 示例用法
    my_list = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']
    new_list = random_half_list(my_list)
    print(new_list)