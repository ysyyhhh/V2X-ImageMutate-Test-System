from django.urls import path
from .views import *





urlpatterns = [
    # 添加扩增任务
    path('execute_aug_task/', execute_aug_task, name='execute_aug_task'),

    # 添加扩增任务
    path('get_all_aug_task/', get_all_aug_task, name='get_all_aug_task'),

    path('get_aug_visual_result/', get_aug_visual_result, name='get_aug_visual_result'),

    path('get_raw_visual_result/', get_raw_visual_result, name='get_raw_visual_result'),

    path('delete_a_aug_task/', delete_a_aug_task, name='delete_a_aug_task'),

    path('get_a_aug_task_info/', get_a_aug_task_info, name='get_a_aug_task_info'),


]