from io import BytesIO

import cv2
import numpy as np

from PIL import Image, ImageOps

from wand.image import Image as WandImage


# 运动模糊扩增
from data_aug.tools.file_tools import get_all_camera_ph


def motion_blur_aug(task_obj, config_obj, target_dir):
    print('--------------------------------------0')
    # 是否分别对不同车辆数据进行扩增
    separate_flag = config_obj.separate_flag

    file_list = get_all_camera_ph(target_dir, separate_flag)

    default_flag = config_obj.default_flag
    aug_para = config_obj.aug_para

    fog = MotionBlur()


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



class MotionBlur:
    def __init__(self, rng=None):
        self.rng = np.random.default_rng() if rng is None else rng

    def __call__(self, img, mag=-1, prob=1.):
        if self.rng.uniform(0, 1) > prob:
            return img

        n_channels = len(img.getbands())
        isgray = n_channels == 1
        # c = [(10, 3), (15, 5), (15, 8), (15, 12), (20, 15)]
        c = [(10, 3), (15, 8),  (20, 15)]
        if mag < 0 or mag >= len(c):
            index = self.rng.integers(0, len(c))
        else:
            index = mag
        c = c[index]

        output = BytesIO()
        img.save(output, format='PNG')
        img = WandImage(blob=output.getvalue())

        img.motion_blur(radius=c[0], sigma=c[1], angle=self.rng.uniform(-45, 45))
        img = cv2.imdecode(np.frombuffer(img.make_blob(), np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(img.astype(np.uint8))

        if isgray:
            img = ImageOps.grayscale(img)

        return img


if __name__ == '__main__':
    img = Image.open('1.png')
    fog = MotionBlur()

    img = fog(img, mag=2, prob=1)
    # 保存输出图像
    img.save('1_MotionBlur.png')