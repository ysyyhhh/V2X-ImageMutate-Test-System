
import cv2

from data_aug.tools.file_tools import get_all_camera_ph

# 模糊扩增
def vague_aug(task_obj, config_obj, target_dir):
    print('--------------------------------------1')
    # 中心车辆id号
    ego_car_id = config_obj.ego_car_id
    # 是否分别对不同车辆数据进行扩增
    separate_flag = config_obj.separate_flag

    file_list = get_all_camera_ph(target_dir, separate_flag)

    default_flag = config_obj.default_flag
    aug_para1 = config_obj.aug_para1
    aug_para2 = config_obj.aug_para2

    for file in file_list:
        # 使用默认参数
        if (default_flag):
            gaussian_blur(file, file)

# 图像模糊处理
def gaussian_blur(input_path, output_path):
    # 读取图片
    img = cv2.imread(input_path)

    # 用高斯模糊函数对图像进行高斯模糊
    # 第一个参数是原始图片，第二个参数是窗口大小，第三个参数是高斯核函数的标准差
    img_blur = cv2.GaussianBlur(img, (5, 5), 4.5)
    # 保存图片
    cv2.imwrite(output_path, img_blur)