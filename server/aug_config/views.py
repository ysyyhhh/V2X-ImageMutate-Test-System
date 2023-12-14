import json

from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from file_up_down.models import PhtotDataModel
from .models import AugConfig,AugTask

@csrf_exempt
def get_all_aug_task(request):
    if request.method == 'GET':

        content = {"status": 0, "msg": "ok", "data": {"count": 0, "rows": []}}

        if request.method == 'GET':
            userid = request.GET.get('userid', "")
            dobjs = AugTask.objects.filter(user_id=int(userid))
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
                mp_temp["raw_file_id"] = obj.raw_file_id
                mp_temp["aug_file_id"] = obj.aug_file_id
                mp_temp["task_state"] = obj.task_state
                mp_temp["config_id"] = obj.config_id
                mp_temp["create_time"] = obj.create_time
                mp_temp["start_time"] = obj.start_time
                mp_temp["end_time"] = obj.end_time
                content["data"]["rows"].append(mp_temp)

            return JsonResponse(content, safe=True)
        else:
            content = {"success": "0", "error": ""}
            return JsonResponse(content, safe=True)

@csrf_exempt
def add_aug_task(request):
    if request.method == 'POST':


        json_str = request.body.decode()
        print(json_str)
        json_dict = json.loads(json_str,encoding='utf-8')
        print(json_dict)

        file_id = json_dict["fileid"]
        file_id = int(file_id)
        aug_type = json_dict["func_select"]
        aug_type = int(aug_type)
        taskname = json_dict["taskname"]

        ego_car_id = json_dict["ego_car_id"]
        ego_car_id = int(ego_car_id)
        separate_flag = json_dict["separate_flag"]


        print('aug_type----------------------------')
        print(aug_type)
        print('file_id----------------------------')
        print(file_id)
        print('taskname----------------------------')
        print(taskname)
        print('ego_car_id----------------------------')
        print(ego_car_id)
        print('separate_flag----------------------------')
        print(separate_flag)

        if(aug_type>5):
            aug_para = json_dict["intensity"]

            print('aug_para----------------------------')
            print(aug_para)


        # 若当前数据库中没有数据，则max_file_id设置为0
        data_count = AugConfig.objects.count()
        if (data_count == 0):
            max_config_id = 0
        else:
            # 获取当前数据库中最大的file_id
            max_config_id = AugConfig.objects.aggregate(max_config_id=Max('config_id'))['max_config_id']

        cur_config_id = max_config_id+1

        register_aug_config_db(json_dict,cur_config_id,ego_car_id,separate_flag)

        register_aug_task_db(file_id, cur_config_id, taskname)

        content = {
            "status": 0,
            "msg": "任务添加成功！"
        }
        # 提示上传成功
        print('------------------------------------------------------------------3')
        return JsonResponse(content, safe=True)

    else:
        content = {
            "status": 1,
            "msg": "任务添加失败！"
        }
        # 提示上传失败
        return JsonResponse(content, safe=True)


aug_type_list = ['Shadow','MotionBlur','HighTemperature','Fog','Rain','Snow']
# 注册扩增配置数据库
def register_aug_config_db(json_dict,config_id,ego_car_id,separate_flag):

    file_id = json_dict["fileid"]
    file_id = int(file_id)
    aug_type = json_dict["func_select"]
    aug_type = int(aug_type)
    taskname = json_dict["taskname"]


    if (aug_type >= 6):
        aug_para = json_dict["intensity"]

        default_flag = False
        aug_type_str = aug_type_list[aug_type-6]
    else:
        aug_para = 0

        default_flag = True
        aug_type_str = aug_type_list[aug_type]

    obj = AugConfig(config_id=config_id, default_flag=default_flag, aug_type=aug_type_str, aug_para=aug_para,
                         ego_car_id=ego_car_id,separate_flag=separate_flag)
    obj.save()

    print('register aug config database succeed!')



# 注册扩增任务数据库
def register_aug_task_db(file_id, config_id,taskname):
    # 若当前数据库中没有数据，则max_file_id设置为0
    data_count = AugTask.objects.count()
    if (data_count == 0):
        max_task_id = 0
    else:
        # 获取当前数据库中最大的task_id
        max_task_id = AugTask.objects.aggregate(max_task_id=Max('task_id'))['max_task_id']

    photo = PhtotDataModel.objects.get(file_id=file_id)
    user_id = photo.user_id

    obj = AugTask(task_id=max_task_id+1, task_name=taskname, user_id=user_id, raw_file_id=file_id,
                    task_state='ready',config_id=config_id)
    obj.save()

    print('register aug task database succeed!')