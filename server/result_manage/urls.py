from django.urls import path
from .views import *
urlpatterns = [

    path('get_all_test_result/', get_all_test_result, name='get_all_test_result'),

    path('get_test_visual_result/', get_test_visual_result, name='get_test_visual_result'),

    path('get_test_num_result/', get_test_num_result, name='get_test_num_result'),

    path('get_test_chart_result/', get_test_chart_result, name='get_test_chart_result'),

    path('get_influence_strong_frames/', get_influence_strong_frames, name='get_influence_strong_frames'),

]