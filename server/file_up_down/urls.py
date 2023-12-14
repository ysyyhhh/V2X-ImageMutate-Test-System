from django.urls import path
from .views import *
urlpatterns = [
    # 上传
    path('upload/', file_upload, name='upload'),


    # 获取文件列表
    path('getAllFile/', get_file_list, name='get_file_list'),
    # 获取指定文件类型的文件列表
    path('get_type_file_list/', get_type_file_list, name='get_type_file_list'),

    # test
    path('test/', test_view, name='test')
]