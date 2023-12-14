import os

from django.test import TestCase

# Create your tests here.
from TestSystemServer.settings import BASE_DIR


def get_camera0_paths(father_path,merge_photo_path):
    camera0_paths = []
    for root, dirs, files in os.walk(merge_photo_path):
        for file in files:
            if file.endswith("camera0.png"):
                camera0_paths.append(os.path.relpath(os.path.join(root, file), father_path))
    return camera0_paths


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


if __name__ == '__main__':
    father_path = os.path.join(BASE_DIR, 'static/aug_file')
    path = os.path.join(BASE_DIR,'static/aug_file/3/test/')
    print(os.listdir(father_path))

    count = 0
    list_ = []
    for item in os.listdir(path):
        temp_path = os.path.join(path, item)
        for item1 in os.listdir(temp_path):
            temp_path1 = os.path.join(temp_path, item1)
            temp_path2 = os.path.join(temp_path1, os.listdir(temp_path1)[count])
            photo_names = get_camera0_paths(path, temp_path2)
            for idx, photo_name in enumerate(photo_names):
                aug_photo_path = os.path.join('/api/static/aug_file', str(3),
                                              'test',
                                              photo_name)

                list_.append(aug_photo_path)
        count = count + 1
    print(list_)