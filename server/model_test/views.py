from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
import threading

from aug_config.models import AugTask, AugConfig
from file_up_down.models import PhtotDataModel
from model_test.models import ModelTestTask
from opencood.tools.inference_camera import inference_data
from TestSystemServer.settings import BASE_DIR
import os
from django.utils import timezone

from opencood.tools.merge_dynamic_static import merge_dynamic_static
from result_manage.models import TestResult, IouData


@csrf_exempt
def get_test_task_list(request):
    if request.method == 'GET':

        content = {"status": 0, "msg": "ok", "data": {"count": 0, "rows": []}}

        if request.method == 'GET':
            userid = request.GET.get('userid', "")
            dobjs = ModelTestTask.objects.filter(user_id=int(userid))
            print('----------------------------------------------dobjs')
            #print(dobjs[0].user_id)
            count = len(dobjs)
            content["data"]["count"] = count

            for idx, obj in enumerate(dobjs):
                print('----------------------------------------------obj')
                print(obj)
                mp_temp = {}

                mp_temp["task_id"] = obj.task_id
                mp_temp["task_name"] = obj.task_name
                mp_temp["user_id"] = obj.user_id
                mp_temp["file_id"] = obj.file_id
                mp_temp["aug_id"] = obj.aug_id
                mp_temp["task_state"] = obj.task_state
                mp_temp["start_time"] = obj.start_time
                mp_temp["end_time"] = obj.end_time
                mp_temp["create_time"] = obj.create_time

                content["data"]["rows"].append(mp_temp)

            return JsonResponse(content, safe=True)
        else:
            content = {"success": "0", "error": ""}
            return JsonResponse(content, safe=True)

# result_path = os.path.join(BASE_DIR, 'static/test_result', str(task_obj.user_id),file_name)
def test_func(task_id, file_path, result_path, ego_id, separate_flag, result_id):
    # t = threading.Thread(target=inference_data, args=(obj, int(userid)))

    model_dir_dynamic = 'opencood/logs/cobevt'
    model_dir_dynamic = os.path.join(BASE_DIR, model_dir_dynamic)

    model_dir_static = 'opencood/logs/cobevt_static'
    model_dir_static = os.path.join(BASE_DIR, model_dir_static)

    validate_dir = file_path
    print('validate_dir----------------------------------------------')
    print(validate_dir)

    result_path_dynamic = os.path.join(result_path, 'dynamic')
    result_path_static = os.path.join(result_path, 'static')
    result_path_merge = os.path.join(result_path, 'merge')

    if not os.path.exists(result_path_dynamic):
        os.makedirs(result_path_dynamic)
    if not os.path.exists(result_path_static):
        os.makedirs(result_path_static)



    # 推理原始数据
    test_task_objs = ModelTestTask.objects.filter(task_id=task_id)
    test_task_obj = test_task_objs[0]
    aug_id = test_task_obj.aug_id
    aug_task_obj = AugTask.objects.get(task_id=aug_id)
    raw_file_id = aug_task_obj.raw_file_id
    raw_file_obj = PhtotDataModel.objects.get(file_id=raw_file_id)
    raw_file_path = raw_file_obj.file_path
    print('---------------------------------------------raw_file_path')
    print(raw_file_path)
    print('---------------------------------------------------ego_id')
    print(ego_id)
    _, _, raw_dynamic_ave_iou = inference_data(model_dir_dynamic, raw_file_path, '', 'dynamic', False, ego_id)
    raw_static_ave_iou, raw_lane_ave_iou, _ = inference_data(model_dir_static, raw_file_path, '', 'static', False, ego_id)

    # 将iou数据写入数据库
    for i in range(len(raw_dynamic_ave_iou)):
        data_count = IouData.objects.count()
        if (data_count == 0):
            max_data_id = 0
        else:
            max_data_id = IouData.objects.aggregate(max_data_id=Max('data_id'))['max_data_id']
        obj = IouData(data_id=max_data_id + 1, result_id=result_id, ego_id=ego_id, car_id=0,
                      data_type='raw', road_iou=raw_static_ave_iou[i], lane_iou=raw_lane_ave_iou[i],
                      dynamic_iou=raw_dynamic_ave_iou[i],frame_id=i)
        obj.save()


    count = 0
    for item in os.listdir(validate_dir):
        count = count+1
        validate_child_dir = os.path.join(validate_dir, item)

        if(separate_flag):
            result_child_path_dynamic = os.path.join(result_path_dynamic, 'car_'+str(count))
            result_child_path_static = os.path.join(result_path_static, 'car_'+str(count))
            result_child_path_merge = os.path.join(result_path_merge, 'car_' + str(count))
        else:
            result_child_path_dynamic = os.path.join(result_path_dynamic, 'car_all' )
            result_child_path_static = os.path.join(result_path_static, 'car_all' )
            result_child_path_merge = os.path.join(result_path_merge, 'car_all')

        if not os.path.exists(result_child_path_dynamic):
            os.makedirs(result_child_path_dynamic)
        if not os.path.exists(result_child_path_static):
            os.makedirs(result_child_path_static)


        # 推理扩增数据
        _, _, aug_dynamic_ave_iou = inference_data(model_dir_dynamic, validate_child_dir, result_child_path_dynamic,
                                                   'dynamic', True, ego_id)
        aug_static_ave_iou, aug_lane_ave_iou, _ = inference_data(model_dir_static, validate_child_dir, result_child_path_static,
                                                                 'static', True, ego_id)
        merge_dynamic_static(result_child_path_dynamic, result_child_path_static, result_child_path_merge)

        # 将iou数据写入数据库
        for i in range(len(aug_dynamic_ave_iou)):
            data_count = IouData.objects.count()
            if (data_count == 0):
                max_data_id = 0
            else:
                max_data_id = IouData.objects.aggregate(max_data_id=Max('data_id'))['max_data_id']
            obj = IouData(data_id=max_data_id + 1, result_id=result_id, ego_id=ego_id, car_id=count,
                                 data_type='aug', road_iou=aug_static_ave_iou[i], lane_iou=aug_lane_ave_iou[i],
                          dynamic_iou=aug_dynamic_ave_iou[i],frame_id=i)
            obj.save()


    #test_task_obj.update(end_time=timezone.now(), task_state='finish')

    ModelTestTask.objects.filter(task_id=task_id).update(end_time=timezone.now(), task_state='finish')


@csrf_exempt
def execute_test_task(request):
    if request.method == 'POST':

        task_id = request.GET.get('task_id', "")
        task_id = int(task_id)
        test_task_objs = ModelTestTask.objects.filter(task_id=task_id)
        test_task_obj = test_task_objs[0]

        ModelTestTask.objects.filter(task_id=task_id).update(start_time=timezone.now(),task_state='running')

        aug_task_id = test_task_obj.aug_id
        aug_task_obj = AugTask.objects.get(task_id=aug_task_id)
        config_obj = AugConfig.objects.get(config_id=aug_task_obj.config_id)
        ego_car_id = config_obj.ego_car_id
        separate_flag = config_obj.separate_flag

        file_id = test_task_obj.file_id
        file_objs = PhtotDataModel.objects.filter(file_id=file_id)
        file_obj = file_objs[0]

        result_id = test_task_obj.result_id
        result_obj = TestResult.objects.get(result_id=result_id)

        file_path = file_obj.file_path

        result_path = result_obj.result_path

        t = threading.Thread(target=test_func,args=(task_id,file_path,result_path,ego_car_id-1,separate_flag,result_id))
        t.start()

        content = {
            "status": 0,
            "msg": "模型测试任务开始执行！",
        }

        return JsonResponse(content, safe=False)

@csrf_exempt
def delete_a_test_task(request):
    if request.method == 'POST':

        task_id = request.GET.get('task_id', "")
        task_id = int(task_id)
        print('task_id------------------------------------------------------------------')
        print(task_id)


        test_task_obj = ModelTestTask.objects.get(task_id=task_id)  # 获取指定 id 的记录
        test_task_obj.delete()  # 删除记录

        content = {
            "status": 0,
            "msg": "任务已成功删除！",
        }

        # 提示任务已成功删除
        return JsonResponse(content, safe=True)

if __name__ == '__main__':
    model_dir = 'opencood/logs/cobevt'
    model_dir = os.path.join(BASE_DIR,model_dir)
    validate_dir = 'data/opv2v/test'
    validate_dir = os.path.join(BASE_DIR, validate_dir)
    model_type = 'dynamic'
    t = threading.Thread(target=test_func,args=(model_dir, validate_dir, model_type))
    t.start()