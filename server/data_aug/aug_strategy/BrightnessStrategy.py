

from PIL import Image

from data_aug.tools.file_tools import get_all_camera_ph

# 针对亮度扩增
def brightness_aug(task_obj, config_obj, target_dir):
    print('--------------------------------------0')
    file_list = get_all_camera_ph(target_dir)

    default_flag = config_obj.default_flag
    aug_para1 = config_obj.aug_para1
    aug_para2 = config_obj.aug_para2

    for file in file_list:
        # 使用默认参数
        if (default_flag):
            adjust_brightness(100, -80, file, file)
        else:
            adjust_brightness(aug_para1, aug_para2, file, file)

# 图像亮度调整
def adjust_brightness(percentage, brightness_change, input_path, output_path):
    # 打开输入图像
    image = Image.open(input_path)

    # 计算要调整亮度的区域
    width, height = image.size
    left = 0
    top = 0
    right = int(width * percentage / 100)
    bottom = height

    # 提取要调整亮度的区域
    region = image.crop((left, top, right, bottom))

    # 限制亮度变化值在合理范围内
    brightness_change = max(-255, min(255, brightness_change))

    # 调整亮度
    region = region.point(lambda p: max(0, min(255, p + brightness_change)))

    # 将调整后的区域放回原图像
    image.paste(region, (left, top, right, bottom))

    # 保存输出图像
    image.save(output_path)