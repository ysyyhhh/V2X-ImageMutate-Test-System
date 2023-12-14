import cv2
import numpy as np

from data_aug.tools.file_tools import get_all_camera_ph

# 椒盐噪声扩增
def noise_aug(task_obj, config_obj, target_dir):
    print('--------------------------------------2')
    # 是否分别对不同车辆数据进行扩增
    separate_flag = config_obj.separate_flag

    file_list = get_all_camera_ph(target_dir, separate_flag)

    default_flag = config_obj.default_flag
    aug_para1 = config_obj.aug_para1
    aug_para2 = config_obj.aug_para2

    for file in file_list:
        # 使用默认参数
        if (default_flag):
            salt_and_pepper_noise(file, file)
        else:
            salt_and_pepper_noise(file, file, aug_para1, aug_para2)



# 添加椒盐噪声   s_vs_p = 0.9-添加椒盐噪声的数目比例   amount = 0.07-添加噪声图像像素的数目
def salt_and_pepper_noise(input_path, output_path, s_vs_p=0.9, amount=0.07):
    # 读取图片
    image = cv2.imread(input_path)
    noisy_img = np.copy(image)
    # 添加salt噪声
    num_salt = np.ceil(amount * image.size * s_vs_p)
    # 设置添加噪声的坐标位置
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_img[coords[0], coords[1], :] = [255, 255, 255]
    # 添加pepper噪声
    num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
    # 设置添加噪声的坐标位置
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_img[coords[0], coords[1], :] = [0, 0, 0]
    # 保存图片
    cv2.imwrite(output_path, noisy_img)