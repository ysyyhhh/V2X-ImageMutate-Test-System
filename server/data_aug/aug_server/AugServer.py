import os
import threading

from django.db.models import Max

from TestSystemServer.settings import BASE_DIR
from aug_config.models import AugTask, AugConfig
from data_aug.aug_server.DataBaseServer import DataBaseServer
from data_aug.aug_strategy import AugStrategy
from data_aug.tools.file_tools import get_camera0_paths, get_all_camera_ph, copy_file, timestamp_to_string
from file_up_down.models import PhtotDataModel
from model_test.models import ModelTestTask
from result_manage.models import TestResult

import time
from django.utils import timezone

db_server = DataBaseServer()



class AugServer:
    def __init__(self):

        return


    def get_aug_visual_result(self,task_id):

        aug_task_obj = db_server.get_aug_task_info(task_id=task_id)
        config_obj = db_server.get_config_info(config_id=aug_task_obj.config_id)
        separate_flag = config_obj.separate_flag

        user_id = aug_task_obj.user_id
        aug_file_id = aug_task_obj.aug_file_id
        raw_file_id = aug_task_obj.raw_file_id

        aug_file_obj = db_server.get_phtot_data(file_id=aug_file_id)
        raw_file_obj = db_server.get_phtot_data(file_id=raw_file_id)

        aug_file_name = aug_file_obj.file_name
        raw_file_name = raw_file_obj.file_name

        aug_file_path = aug_file_obj.file_path
        raw_file_path = raw_file_obj.file_path

        aug_photo_path_list = []

        if (separate_flag):
            count = 0
            for item in os.listdir(aug_file_path):
                temp_path = os.path.join(aug_file_path, item)
                for item1 in os.listdir(temp_path):
                    temp_path1 = os.path.join(temp_path, item1)
                    temp_path2 = os.path.join(temp_path1, os.listdir(temp_path1)[count])
                    photo_names = get_camera0_paths(aug_file_path, temp_path2)
                    for idx, photo_name in enumerate(photo_names):
                        aug_photo_path = os.path.join('/api/static/aug_file', str(user_id),
                                                      aug_file_name,
                                                      photo_name)

                        aug_photo_path_list.append(aug_photo_path)
                count = count + 1
        else:
            photo_names = get_camera0_paths(aug_file_path, aug_file_path)
            for idx, photo_name in enumerate(photo_names):
                aug_photo_path = os.path.join('/api/static/aug_file', str(user_id), aug_file_name,
                                              photo_name)

                aug_photo_path_list.append(aug_photo_path)

        return aug_photo_path_list


    def get_raw_visual_result(self,task_id):
        aug_task_obj = db_server.get_aug_task_info(task_id=task_id)

        user_id = aug_task_obj.user_id
        aug_file_id = aug_task_obj.aug_file_id
        raw_file_id = aug_task_obj.raw_file_id

        aug_file_obj = db_server.get_phtot_data(file_id=aug_file_id)
        raw_file_obj = db_server.get_phtot_data(file_id=raw_file_id)

        aug_file_name = aug_file_obj.file_name
        raw_file_name = raw_file_obj.file_name

        aug_file_path = aug_file_obj.file_path
        raw_file_path = raw_file_obj.file_path

        photo_names = get_camera0_paths(raw_file_path, raw_file_path)

        raw_photo_path_list = []
        for idx, photo_name in enumerate(photo_names):
            aug_photo_path = os.path.join('/api/static/static', str(user_id), raw_file_name,
                                          photo_name)

            raw_photo_path_list.append(aug_photo_path)

        return raw_photo_path_list

    def get_all_aug_task(self,user_id):
        aug_task_objs = db_server.get_finish_aug_tasks_info(user_id=user_id)

        res_list = []
        for idx, obj in enumerate(aug_task_objs):
            print('----------------------------------------------obj')
            print(obj)
            mp_temp = {}

            mp_temp["label"] = '扩增任务 - ' + str(obj.task_id)
            mp_temp["value"] = obj.task_id

            res_list.append(mp_temp)
        return res_list

    def execute_aug_task(self,task_id):
        task_obj = db_server.get_aug_task_info(task_id=task_id)


        config_id = task_obj.config_id
        config_id = int(config_id)
        print('config_id------------------------------------------------------------------')
        print(config_id)

        config_obj = db_server.get_config_info(config_id=config_id)


        t = threading.Thread(target=self.aug_func, args=(task_obj, config_obj))
        t.start()

    def aug_func(self,task_obj, config_obj):
        # 更新扩增任务状态和开始时间

        db_server.update_aug_task_state(task_id=task_obj.task_id,state='running')

        raw_file_id = task_obj.raw_file_id
        task_name = task_obj.task_name
        aug_id = task_obj.task_id
        # 中心车辆id号
        ego_car_id = config_obj.ego_car_id
        # 是否分别对不同车辆数据进行扩增
        separate_flag = config_obj.separate_flag


        file_obj = db_server.get_phtot_data(file_id=raw_file_id)

        file_name = file_obj.file_name
        file_type = file_obj.file_type
        file_type = int(file_type)
        user_id = file_obj.user_id
        user_id = int(user_id)

        file_name = file_name.split("_")[0]  # 去掉时间戳后缀

        t = time.time()
        file_name += '_'
        file_name += timestamp_to_string(t)

        # 拷贝file_type-1份
        source_dir = os.path.join(BASE_DIR, 'static/static', str(task_obj.user_id), file_obj.file_name)  # 需要copy文件路径
        target_dir = os.path.join(BASE_DIR, 'static/aug_file', str(task_obj.user_id), file_name)  # 目标文件夹路径
        if (separate_flag):
            for i in range(file_type):
                temp_file_name = 'car_' + str(i + 1) + '_aug'
                temp_target_dir = os.path.join(target_dir, temp_file_name)
                copy_file(source_dir, temp_target_dir)
                print('source_dir------------------------------------------------------------------')
                print(source_dir)
                print('target_dir------------------------------------------------------------------')
                print(target_dir)

        else:
            temp_file_name = 'car_all_aug'
            temp_target_dir = os.path.join(target_dir, temp_file_name)
            copy_file(source_dir, temp_target_dir)


        aug_type = config_obj.aug_type
        AugStrategy.data_aug(aug_type, task_obj, config_obj, target_dir)


        # 将扩增的文件记录写入数据库

        max_file_id = db_server.get_max_file_id()

        obj = PhtotDataModel(file_id=max_file_id + 1, user_id=user_id, file_name=file_name, file_type=file_type,
                             file_state='augmented', file_desc=file_obj.file_desc, file_path=target_dir)
        obj.save()

        # 新建模型测试任务，并写入数据库

        max_task_id = db_server.get_max_model_test_task_id()

        result_path = os.path.join(BASE_DIR, 'static/test_result', str(task_obj.user_id), file_name)

        # 新建模型测试结果

        max_result_id = db_server.get_max_result_id()

        obj = ModelTestTask(task_id=max_task_id + 1, task_name=task_name, user_id=user_id, file_id=max_file_id + 1,
                            aug_id=aug_id, task_state='ready', result_id=max_result_id + 1)
        obj.save()

        obj = TestResult(test_task_id=max_task_id + 1, result_id=max_result_id + 1, user_id=user_id,
                         result_path=result_path)
        print('----------------------------------------result_path')
        print(result_path)
        obj.save()

        # 更新扩增任务状态和开始时间、扩增完成文件id号
        db_server.update_aug_task_state(task_id=task_obj.task_id, state='finish',aug_file_id=max_file_id + 1)

    def delete_a_aug_task(self, task_id):

        task_obj = db_server.get_aug_task_info(task_id=task_id)

        config_id = task_obj.config_id
        config_id = int(config_id)
        print('config_id------------------------------------------------------------------')
        print(config_id)

        db_server.delete_a_aug_task(task_id=task_id)
        db_server.delete_a_aug_config(config_id=config_id)



    def get_a_aug_task_info(self, task_id):

        task_obj = db_server.get_aug_task_info(task_id=task_id)

        config_obj = db_server.get_config_info(config_id=task_obj.config_id)

        return (config_obj.ego_car_id,config_obj.separate_flag,config_obj.aug_type,config_obj.aug_para)







