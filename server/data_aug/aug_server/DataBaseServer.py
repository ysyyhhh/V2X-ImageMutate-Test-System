from django.db.models import Max

from aug_config.models import AugTask, AugConfig
from file_up_down.models import PhtotDataModel
from django.utils import timezone

from model_test.models import ModelTestTask
from result_manage.models import TestResult


class DataBaseServer:
    def __init__(self):
        return


    def get_config_info(self,config_id):
        config_obj = AugConfig.objects.get(config_id=config_id)
        return config_obj


    def get_aug_task_info(self,task_id):
        aug_task_obj = AugTask.objects.get(task_id=task_id)
        return aug_task_obj

    def get_finish_aug_tasks_info(self,user_id):
        aug_task_objs = AugTask.objects.filter(user_id=user_id, task_state='finish')
        return aug_task_objs

    def get_phtot_data(self,file_id):
        file_obj = PhtotDataModel.objects.get(file_id=file_id)
        return file_obj

    def update_aug_task_state(self,task_id,state,aug_file_id=0):
        if(state=='running'):
            AugTask.objects.filter(task_id=task_id).update(task_state=state, start_time=timezone.now())
        else:
            AugTask.objects.filter(task_id=task_id).update(task_state=state,
                                                                    end_time=timezone.now(),
                                                                    aug_file_id=aug_file_id)
    def get_max_file_id(self):
        data_count = PhtotDataModel.objects.count()
        if (data_count == 0):
            max_file_id = 0
        else:
            max_file_id = PhtotDataModel.objects.aggregate(max_file_id=Max('file_id'))['max_file_id']
        return max_file_id

    def get_max_model_test_task_id(self):
        data_count = ModelTestTask.objects.count()
        if (data_count == 0):
            max_task_id = 0
        else:
            max_task_id = ModelTestTask.objects.aggregate(max_task_id=Max('task_id'))['max_task_id']
        return max_task_id

    def get_max_result_id(self):
        data_count = TestResult.objects.count()
        if (data_count == 0):
            max_result_id = 0
        else:
            max_result_id = TestResult.objects.aggregate(max_result_id=Max('result_id'))['max_result_id']
        return max_result_id

    def delete_a_aug_task(self, task_id):

        aug_task_obj = AugTask.objects.get(task_id=task_id)  # 获取指定 id 的记录
        aug_task_obj.delete()  # 删除记录

    def delete_a_aug_config(self, config_id):

        aug_config_obj = AugConfig.objects.get(config_id=config_id)  # 获取指定 id 的记录
        aug_config_obj.delete()  # 删除记录

