from django.urls import path
from .views import *
urlpatterns = [
    # 添加扩增任务
    path('add_aug_task/', add_aug_task, name='add_aug_task'),

    # 获取扩增任务列表
    path('get_all_aug_task/', get_all_aug_task, name='get_all_aug_task'),

]