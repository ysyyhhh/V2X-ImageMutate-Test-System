import math
from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from pkg_resources import resource_filename

from data_aug.tools.file_tools import get_all_camera_ph


# 阴影扩增
def rain_aug(task_obj, config_obj, target_dir):
    print('--------------------------------------0')
    # 是否分别对不同车辆数据进行扩增
    separate_flag = config_obj.separate_flag

    file_list = get_all_camera_ph(target_dir, separate_flag)

    default_flag = config_obj.default_flag
    aug_para = config_obj.aug_para

    fog = Rain()


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

class Rain:
    def __init__(self, rng=None):
        self.rng = np.random.default_rng() if rng is None else rng

    def __call__(self, img, mag=-1, prob=1.):
        if self.rng.uniform(0, 1) > prob:
            return img

        img = img.copy()
        w, h = img.size
        n_channels = len(img.getbands())
        isgray = n_channels == 1
        line_width = self.rng.integers(1, 2)

        c = [1000, 8000, 18000]
        if mag < 0 or mag >= len(c):
            index = 0
        else:
            index = mag
        c = c[index]

        n_rains = self.rng.integers(c, c + 20)
        slant = self.rng.integers(-60, 60)
        fillcolor = 200 if isgray else (200, 200, 200)

        draw = ImageDraw.Draw(img)
        max_length = min(w, h, 10)
        for i in range(1, n_rains):
            length = self.rng.integers(5, max_length)
            x1 = self.rng.integers(0, w - length)
            y1 = self.rng.integers(0, h - length)
            x2 = x1 + length * math.sin(slant * math.pi / 180.)
            y2 = y1 + length * math.cos(slant * math.pi / 180.)
            x2 = int(x2)
            y2 = int(y2)
            draw.line([(x1, y1), (x2, y2)], width=line_width, fill=fillcolor)

        return img

if __name__ == '__main__':
    img = Image.open('1.png')
    fog = Rain()

    img = fog(img, mag=2, prob=1)
    # 保存输出图像
    img.save('1_rain.png')