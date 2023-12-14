import os
import shutil
from datetime import datetime

# 将时间戳转换为'2023_06_15_11_54_54_222'这种形式
def timestamp_to_string(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]

def get_camera0_paths(father_path,merge_photo_path):
    camera0_paths = []
    for root, dirs, files in os.walk(merge_photo_path):
        for file in files:
            if file.endswith("camera0.png"):
                camera0_paths.append(os.path.relpath(os.path.join(root, file), father_path))
    return camera0_paths

def copy_file(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        target_file = os.path.join(target_dir, file_name)
        if os.path.isfile(source_file):
            shutil.copy(source_file, target_file)
        elif os.path.isdir(source_file):
            copy_file(source_file, target_file)


# 获取一个路径path下的第一个文件夹下的第x个文件夹的访问路径
def get_folder_path(path, x):
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    if len(folders) > 0:
        first_folder = folders[0]
        subfolders = [f for f in os.listdir(os.path.join(path, first_folder)) if
                      os.path.isdir(os.path.join(path, first_folder, f))]
        if len(subfolders) >= x:
            return os.path.join(path, first_folder, subfolders[x - 1])
    return None


def get_all_camera_ph(target_dir, separate_flag):

    file_list = []
    if (separate_flag):
        temp_dir_list = []
        count = 0
        for item in os.listdir(target_dir):
            if os.path.isdir(os.path.join(target_dir, item)):
                temp_dir_list.append(get_folder_path(os.path.join(target_dir, item), count + 1))
                count += 1

        for child_dir in temp_dir_list:
            for root, dirs, files in os.walk(child_dir):
                for file in files:
                    if file.endswith(('camera0.png', 'camera1.png', 'camera2.png', 'camera3.png')):
                        file_list.append(os.path.join(root, file))
    else:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith(('camera0.png', 'camera1.png', 'camera2.png', 'camera3.png')):
                    file_list.append(os.path.join(root, file))
    return file_list