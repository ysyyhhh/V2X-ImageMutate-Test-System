from django.urls import path
from .views import *
urlpatterns = [
    # 测试模型
    path('execute_test_task/', execute_test_task, name='execute_test_task'),

    path('get_test_task_list/', get_test_task_list, name='get_test_task_list'),

    path('delete_a_test_task/', delete_a_test_task, name='delete_a_test_task'),


]