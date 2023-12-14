import json
import os
import statistics

from django.http import JsonResponse
from django.shortcuts import render



from django.views.decorators.csrf import csrf_exempt

from aug_config.models import AugTask, AugConfig
from file_up_down.models import PhtotDataModel
from model_test.models import ModelTestTask

# 获取已经测试完成的结果列表
from result_manage.models import TestResult, IouData


@csrf_exempt
def get_all_test_result(request):
    if request.method == 'GET':

        content = {"status": 0, "msg": "ok", "data": { "options": []}}

        user_id = request.GET.get('user_id', "")
        user_id = int(user_id)
        test_task_objs = ModelTestTask.objects.filter(user_id=user_id,task_state='finish')




        for idx, obj in enumerate(test_task_objs):
            print('----------------------------------------------obj')
            print(obj)
            mp_temp = {}

            mp_temp["label"] = '测试任务 - '+str(obj.task_id)
            mp_temp["value"] = obj.task_id


            content["data"]["options"].append(mp_temp)



        return JsonResponse(content, safe=True)
    else:
        content = {"success": "0", "error": ""}
        return JsonResponse(content, safe=True)


def get_file_names(merge_photo_path):
    file_names = []
    for file in os.listdir(merge_photo_path):
        if os.path.isfile(os.path.join(merge_photo_path, file)):
            file_names.append(file)
    return file_names

# 获取可视化图像
@csrf_exempt
def get_test_visual_result(request):
    if request.method == 'GET':

        content = {"status": 0, "msg": "ok", "data": { "imageList": []}}

        task_id = request.GET.get('task_id', "")
        if(task_id==''):
            return JsonResponse({}, safe=True)
        task_id = int(task_id)
        test_task_obj = ModelTestTask.objects.get(task_id=task_id)

        user_id = test_task_obj.user_id
        file_id = test_task_obj.file_id
        result_id = test_task_obj.result_id

        file_obj = PhtotDataModel.objects.get(file_id=file_id)

        file_name = file_obj.file_name

        #result_path = test_task_obj.result_path

        # ----------------------------
        result_obj = TestResult.objects.get(result_id=result_id)
        result_path = result_obj.result_path


        merge_photos_path = os.path.join(result_path,'merge')
        photo_names = get_file_names(merge_photos_path)
        print('--------------------------------------photo_names')
        print(photo_names)

        # 没有分车扩增
        if(len(os.listdir(merge_photos_path))==1):
            temp_path = os.path.join(merge_photos_path,os.listdir(merge_photos_path)[0])
            photo_names = get_file_names(temp_path)
            zhenshu = 1
            for idx, photo_name in enumerate(photo_names):
                merge_photo_path = os.path.join('/api/static/test_result', str(user_id), file_name,
                                                'merge', os.listdir(merge_photos_path)[0], photo_name)
                temp = {"image": merge_photo_path,
                        "title": "扩增车辆ID : 全部" ,
                        "description": "图像帧数 : " + str(zhenshu)}
                content["data"]["imageList"].append(temp)
                zhenshu += 1
        # 进行了分车扩增
        else:
            count = 1
            car_id = 1
            temp_lists = []
            for dir in os.listdir(merge_photos_path):
                temp_path = os.path.join(merge_photos_path, dir)
                photo_names = get_file_names(temp_path)
                zhenshu = 1
                temp_list = []
                for idx, photo_name in enumerate(photo_names):
                    merge_photo_path = os.path.join('/api/static/test_result', str(user_id), file_name,
                                                    'merge', dir, photo_name)
                    temp = {"image": merge_photo_path,
                            "title": "图像帧数 : "+str(zhenshu),
                            "description": "扩增车辆ID : "+str(car_id)}
                    temp_list.append(temp)
                    count += 1
                    zhenshu += 1
                car_id += 1
                temp_lists.append(temp_list)

            row = len(temp_lists)
            col = len(temp_lists[0])

            for j in range(col):
                for i in range(row):
                    content["data"]["imageList"].append(temp_lists[i][j])

        return JsonResponse(content, safe=True)

# 获取iou数据
@csrf_exempt
def get_test_num_result(request):
    if request.method == 'GET':

        content = {"status": 0, "msg": "ok", "data": {"count": 2,"rows": []}}

        task_id = request.GET.get('task_id', "")
        if (task_id == ''):
            return JsonResponse({}, safe=True)
        task_id = int(task_id)
        test_task_obj = ModelTestTask.objects.get(task_id=task_id)
        aug_id = test_task_obj.aug_id
        aug_task_obj = AugTask.objects.get(task_id=aug_id)

        config_obj = AugConfig.objects.get(config_id=aug_task_obj.config_id)
        separate_flag = config_obj.separate_flag

        file_obj = PhtotDataModel.objects.get(file_id=aug_task_obj.raw_file_id)
        file_type = file_obj.file_type

        result_id = test_task_obj.result_id


        if(separate_flag):
            content["data"]["count"] = file_type+1
            for i in range(file_type):

                iou_objs = IouData.objects.filter(result_id=result_id,data_type='aug',car_id=i+1)

                static_ave_iou = []
                dynamic_ave_iou = []
                lane_ave_iou = []
                ego_id = 0
                for iou_obj in iou_objs:
                    ego_id = iou_obj.ego_id
                    static_ave_iou.append(iou_obj.road_iou)
                    dynamic_ave_iou.append(iou_obj.dynamic_iou)
                    lane_ave_iou.append(iou_obj.lane_iou)

                road_iou = statistics.mean(static_ave_iou)
                dynamic_iou = statistics.mean(dynamic_ave_iou)
                lane_iou = statistics.mean(lane_ave_iou)

                temp1 = {'type': '扩增数据', 'road_iou': road_iou, 'lane_iou': lane_iou,
                         'dynamic_iou': dynamic_iou, 'car_id': i+1, 'ego_id': ego_id}

                content["data"]["rows"].append(temp1)
        else:
            iou_objs = IouData.objects.filter(result_id=result_id, data_type='aug', car_id=1)

            static_ave_iou = []
            dynamic_ave_iou = []
            lane_ave_iou = []
            ego_id = 0
            for iou_obj in iou_objs:
                ego_id = iou_obj.ego_id
                static_ave_iou.append(iou_obj.road_iou)
                dynamic_ave_iou.append(iou_obj.dynamic_iou)
                lane_ave_iou.append(iou_obj.lane_iou)

            road_iou = statistics.mean(static_ave_iou)
            dynamic_iou = statistics.mean(dynamic_ave_iou)
            lane_iou = statistics.mean(lane_ave_iou)

            temp1 = {'type': '扩增数据', 'road_iou': road_iou, 'lane_iou': lane_iou,
                     'dynamic_iou': dynamic_iou, 'car_id': '所有', 'ego_id': ego_id}

            content["data"]["rows"].append(temp1)


        # 原始数据
        iou_objs = IouData.objects.filter(result_id=result_id, data_type='raw')

        static_ave_iou = []
        dynamic_ave_iou = []
        lane_ave_iou = []
        ego_id = 0
        for iou_obj in iou_objs:
            ego_id = iou_obj.ego_id
            static_ave_iou.append(iou_obj.road_iou)
            dynamic_ave_iou.append(iou_obj.dynamic_iou)
            lane_ave_iou.append(iou_obj.lane_iou)

        road_iou = statistics.mean(static_ave_iou)
        dynamic_iou = statistics.mean(dynamic_ave_iou)
        lane_iou = statistics.mean(lane_ave_iou)

        temp1 = {'type': '原始数据', 'road_iou': road_iou, 'lane_iou': lane_iou,
                 'dynamic_iou': dynamic_iou, 'car_id': '无', 'ego_id': ego_id}

        content["data"]["rows"].append(temp1)



        return JsonResponse(content, safe=True)

# 获取chart数据
@csrf_exempt
def get_test_chart_result(request):
    if request.method == 'GET':

        content = {"status": 0, "msg": "ok", "data": {}}

        data_list = []

        task_id = request.GET.get('task_id', "")
        if (task_id == ''):
            return JsonResponse({}, safe=True)
        task_id = int(task_id)
        test_task_obj = ModelTestTask.objects.get(task_id=task_id)
        aug_id = test_task_obj.aug_id
        aug_task_obj = AugTask.objects.get(task_id=aug_id)

        config_obj = AugConfig.objects.get(config_id=aug_task_obj.config_id)
        separate_flag = config_obj.separate_flag

        file_obj = PhtotDataModel.objects.get(file_id=aug_task_obj.raw_file_id)
        file_type = file_obj.file_type

        result_id = test_task_obj.result_id

        if (separate_flag):
            content["data"]["count"] = file_type + 1
            for i in range(file_type):

                iou_objs = IouData.objects.filter(result_id=result_id, data_type='aug', car_id=i + 1)

                static_ave_iou = []
                dynamic_ave_iou = []
                lane_ave_iou = []
                ego_id = 0
                for iou_obj in iou_objs:
                    ego_id = iou_obj.ego_id
                    static_ave_iou.append(iou_obj.road_iou)
                    dynamic_ave_iou.append(iou_obj.dynamic_iou)
                    lane_ave_iou.append(iou_obj.lane_iou)

                road_iou = statistics.mean(static_ave_iou)
                dynamic_iou = statistics.mean(dynamic_ave_iou)
                lane_iou = statistics.mean(lane_ave_iou)


                content["data"]["aug" + str(i + 1)] = [road_iou, lane_iou, dynamic_iou]
                data_list.append("aug" + str(i + 1))
        else:
            iou_objs = IouData.objects.filter(result_id=result_id, data_type='aug', car_id=1)

            static_ave_iou = []
            dynamic_ave_iou = []
            lane_ave_iou = []
            ego_id = 0
            for iou_obj in iou_objs:
                ego_id = iou_obj.ego_id
                static_ave_iou.append(iou_obj.road_iou)
                dynamic_ave_iou.append(iou_obj.dynamic_iou)
                lane_ave_iou.append(iou_obj.lane_iou)

            road_iou = statistics.mean(static_ave_iou)
            dynamic_iou = statistics.mean(dynamic_ave_iou)
            lane_iou = statistics.mean(lane_ave_iou)


            content["data"]["aug_all"] = [road_iou, lane_iou, dynamic_iou]
            data_list.append("aug_all")

        # 原始数据
        iou_objs = IouData.objects.filter(result_id=result_id, data_type='raw')

        static_ave_iou = []
        dynamic_ave_iou = []
        lane_ave_iou = []
        ego_id = 0
        for iou_obj in iou_objs:
            ego_id = iou_obj.ego_id
            static_ave_iou.append(iou_obj.road_iou)
            dynamic_ave_iou.append(iou_obj.dynamic_iou)
            lane_ave_iou.append(iou_obj.lane_iou)

        road_iou = statistics.mean(static_ave_iou)
        dynamic_iou = statistics.mean(dynamic_ave_iou)
        lane_iou = statistics.mean(lane_ave_iou)

        data_list.append("raw")
        content["data"]["raw"] = [road_iou, lane_iou, dynamic_iou]

        content["data"]["data_list"] = data_list

        return JsonResponse(content, safe=True)

# 获取chart数据
@csrf_exempt
def get_influence_strong_frames(request):
    if request.method == 'GET':

        content = {"status": 0,"msg": "ok","data":{"count": 0,"rows": []}}

        data_list = []

        task_id = request.GET.get('task_id', "")
        param1 = request.GET.get('param1', "")
        param2 = request.GET.get('param2', "")
        param3 = request.GET.get('param3', "")
        if (task_id == ''):
            return JsonResponse(content, safe=True)
        if (param1 == ''):
            return JsonResponse(content, safe=True)
        if (param2 == ''):
            return JsonResponse(content, safe=True)
        if (param3 == ''):
            return JsonResponse(content, safe=True)

        task_id = int(task_id)
        param1 = float(param1)
        param2 = float(param2)
        param3 = float(param3)

        test_task_obj = ModelTestTask.objects.get(task_id=task_id)
        aug_id = test_task_obj.aug_id
        aug_task_obj = AugTask.objects.get(task_id=aug_id)

        config_obj = AugConfig.objects.get(config_id=aug_task_obj.config_id)
        separate_flag = config_obj.separate_flag

        file_obj = PhtotDataModel.objects.get(file_id=aug_task_obj.raw_file_id)
        file_type = file_obj.file_type

        result_id = test_task_obj.result_id

        # 原始数据
        iou_objs = IouData.objects.filter(result_id=result_id, data_type='raw').order_by('frame_id')

        raw_static_ave_iou = []
        raw_dynamic_ave_iou = []
        raw_lane_ave_iou = []
        ego_id = 0
        for iou_obj in iou_objs:
            ego_id = iou_obj.ego_id
            raw_static_ave_iou.append(iou_obj.road_iou)
            raw_dynamic_ave_iou.append(iou_obj.dynamic_iou)
            raw_lane_ave_iou.append(iou_obj.lane_iou)

        if (separate_flag):

            count = 0
            for i in range(file_type):

                iou_objs = IouData.objects.filter(result_id=result_id, data_type='aug', car_id=i + 1).order_by('frame_id')

                aug_file_id = aug_task_obj.aug_file_id
                file_obj = PhtotDataModel.objects.get(file_id=aug_file_id)
                file_path = file_obj.file_path
                file_path = os.path.join(file_path, 'car_'+str(i + 1)+'_aug')
                file_list = find_camera_files(file_path)


                for i in range(len(iou_objs)):
                    iou_obj = iou_objs[i]
                    if (raw_static_ave_iou[i] - iou_obj.road_iou > param1
                            and raw_lane_ave_iou[i] - iou_obj.lane_iou > param2
                            and raw_dynamic_ave_iou[i] - iou_obj.dynamic_iou > param3):
                        count += 1
                        mp_temp = {}
                        mp_temp["id"] = count
                        mp_temp["file_name"] = file_list[i]
                        mp_temp["road_iou_down"] = raw_static_ave_iou[i] - iou_obj.road_iou
                        mp_temp["dynamic_iou_down"] = raw_dynamic_ave_iou[i] - iou_obj.dynamic_iou
                        mp_temp["lane_iou_down"] = raw_lane_ave_iou[i] - iou_obj.lane_iou
                        mp_temp["car_id"] = i + 1
                        content["data"]["rows"].append(mp_temp)
                content["data"]["count"] = count

        else:
            iou_objs = IouData.objects.filter(result_id=result_id, data_type='aug', car_id=1).order_by('frame_id')

            aug_file_id = aug_task_obj.aug_file_id
            file_obj = PhtotDataModel.objects.get(file_id=aug_file_id)
            file_path = file_obj.file_path
            file_path = os.path.join(file_path,'car_all_aug')
            file_list = find_camera_files(file_path)

            print('--------------------------------file_path')
            print(file_path)
            print('--------------------------------file_list')
            print(file_list)
            count = 0

            for i in range(len(iou_objs)):
                iou_obj = iou_objs[i]
                if(raw_static_ave_iou[i]-iou_obj.road_iou > param1
                        and raw_dynamic_ave_iou[i]-iou_obj.dynamic_iou > param2
                        and raw_lane_ave_iou[i]-iou_obj.lane_iou > param3):
                    count += 1
                    mp_temp = {}
                    mp_temp["id"] = count
                    mp_temp["file_name"] = file_list[i]
                    mp_temp["road_iou_down"] = raw_static_ave_iou[i]-iou_obj.road_iou
                    mp_temp["dynamic_iou_down"] = raw_dynamic_ave_iou[i]-iou_obj.dynamic_iou
                    mp_temp["lane_iou_down"] = raw_lane_ave_iou[i]-iou_obj.lane_iou
                    mp_temp["car_id"] = 'All'
                    content["data"]["rows"].append(mp_temp)
            content["data"]["count"] = count

        return JsonResponse(content, safe=True)

def find_camera_files(path):
    # 获取第一个文件夹
    subfolders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    print('--------------------------------subfolders')
    print(subfolders)
    if len(subfolders) > 0:
        subfolder_path = os.path.join(path, subfolders[0])
    else:
        return []  # 如果没有子文件夹，则返回空列表

    # 获取第一个文件夹下的第一个文件夹
    subfolders = [f for f in os.listdir(subfolder_path) if os.path.isdir(os.path.join(subfolder_path, f))]
    print('--------------------------------subfolders')
    print(subfolders)
    if len(subfolders) > 0:
        subfolder_path = os.path.join(subfolder_path, subfolders[0])
    else:
        return []  # 如果没有子文件夹，则返回空列表

    # 获取第一个文件夹下以camera0.png为结尾的文件
    camera_files = [f.split('.')[0][:-1] for f in os.listdir(subfolder_path) if f.endswith("camera0.png")]
    return camera_files