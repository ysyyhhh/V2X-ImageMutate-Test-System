import numpy as np

from PIL import Image

# 阴影扩增
from data_aug.tools.file_tools import get_all_camera_ph


def speckle_noise_aug(task_obj, config_obj, target_dir):
    print('--------------------------------------0')
    # 是否分别对不同车辆数据进行扩增
    separate_flag = config_obj.separate_flag

    file_list = get_all_camera_ph(target_dir, separate_flag)

    default_flag = config_obj.default_flag
    aug_para = config_obj.aug_para

    fog = SpeckleNoise()


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


class SpeckleNoise:
    def __init__(self, rng=None):
        self.rng = np.random.default_rng() if rng is None else rng

    def __call__(self, img, mag=-1, prob=1.):
        if self.rng.uniform(0, 1) > prob:
            return img

        # c = self.rng.uniform(.15, .6)
        b = [.15, .2, .25]
        if mag < 0 or mag >= len(b):
            index = 0
        else:
            index = mag
        a = b[index]
        c = self.rng.uniform(a, a + .05)
        img = np.asarray(img) / 255.
        img = np.clip(img + img * self.rng.normal(size=img.shape, scale=c), 0, 1) * 255
        return Image.fromarray(img.astype(np.uint8))

if __name__ == '__main__':
    img = Image.open('1.png')
    fog = SpeckleNoise()

    img = fog(img, mag=2, prob=1)
    # 保存输出图像
    img.save('1_SpeckleNoise.png')