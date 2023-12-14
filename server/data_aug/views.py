import os
import shutil
import threading

import cv2
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# 获取所有文件
from django.views.decorators.csrf import csrf_exempt

from TestSystemServer.settings import BASE_DIR
from aug_config.models import AugTask, AugConfig
from data_aug.aug_server.AugServer import AugServer
from data_aug.tools.file_tools import get_camera0_paths
from file_up_down.models import PhtotDataModel
import time
from datetime import datetime

from django.db import models
from django.utils import timezone

from model_test.models import ModelTestTask
from result_manage.models import TestResult
from PIL import Image
import numpy as np


aug_server = AugServer()

@csrf_exempt
def get_aug_visual_result(request):
    if request.method == 'GET':



        content = {"status": 0, "msg": "ok", "data": { "imageList": []}}

        task_id = request.GET.get('task_id', "")
        if(task_id==''):
            return JsonResponse({}, safe=True)
        task_id = int(task_id)
        aug_photo_path_list = aug_server.get_aug_visual_result(task_id)

        content["data"]["imageList"] = aug_photo_path_list

        return JsonResponse(content, safe=True)


@csrf_exempt
def get_raw_visual_result(request):

    if request.method == 'GET':

        content = {"status": 0, "msg": "ok", "data": { "imageList": []}}

        task_id = request.GET.get('task_id', "")
        if(task_id==''):
            return JsonResponse({}, safe=True)
        task_id = int(task_id)
        raw_photo_path_list = aug_server.get_raw_visual_result(task_id)

        content["data"]["imageList"] = raw_photo_path_list

        return JsonResponse(content, safe=True)


@csrf_exempt
def get_all_aug_task(request):
    if request.method == 'GET':

        content = {"status": 0, "msg": "ok", "data": { "options": []}}

        user_id = request.GET.get('user_id', "")
        user_id = int(user_id)

        res_list = aug_server.get_all_aug_task(user_id)

        content["data"]["options"] = res_list

        return JsonResponse(content, safe=True)
    else:
        content = {"success": "0", "error": ""}
        return JsonResponse(content, safe=True)


@csrf_exempt
def execute_aug_task(request):
    if request.method == 'POST':

        task_id = request.GET.get('task_id', "")
        task_id = int(task_id)
        print('task_id------------------------------------------------------------------')
        print(task_id)

        dobjs = AugTask.objects.filter(task_id=task_id)

        task_obj = dobjs[0]

        if(task_obj.task_state=='finish'):
            content = {
                "status": 1,
                "msg": "扩增任务已经执行完成，无须再次扩增",
            }

            # 提示开始数据扩增
            return JsonResponse(content, safe=True)

        aug_server.execute_aug_task(task_id)

        content = {
            "status": 0,
            "msg": "扩增任务开始执行！",
        }

        # 提示开始数据扩增
        return JsonResponse(content, safe=True)



@csrf_exempt
def delete_a_aug_task(request):
    if request.method == 'POST':

        task_id = request.GET.get('task_id', "")
        task_id = int(task_id)
        print('task_id------------------------------------------------------------------')
        print(task_id)

        aug_server.delete_a_aug_task(task_id)

        content = {
            "status": 0,
            "msg": "任务已成功删除！",
        }

        # 提示任务已成功删除
        return JsonResponse(content, safe=True)



def get_a_aug_task_info(request):
    if request.method == 'GET':

        task_id = request.GET.get('task_id', "")
        task_id = int(task_id)
        print('task_id------------------------------------------------------------------')
        print(task_id)

        ego_car_id,separate_flag,aug_type,aug_para = aug_server.get_a_aug_task_info(task_id=task_id)

        content = {"status": 0, "msg": "ok", "data": { }}

        # res_list = aug_server.get_a_aug_task_info(task_id)

        dic = {"a":"test","b":"test","c":"test","d":"test"}

        content["data"]["items"] = [1]
        content["data"]["ego_car_id"] = ego_car_id
        if separate_flag:
            content["data"]["separate_flag"] = "是"
        else:
            content["data"]["separate_flag"] = "否"

        content["data"]["aug_type"] = aug_type
        content["data"]["aug_para"] = aug_para

        if(aug_para==0):
            content["data"]["aug_para"] = "弱"
        elif(aug_para==1):
            content["data"]["aug_para"] = "中"
        else:
            content["data"]["aug_para"] = "强"


        return JsonResponse(content, safe=True)
    else:
        content = {"success": "0", "error": ""}
        return JsonResponse(content, safe=True)