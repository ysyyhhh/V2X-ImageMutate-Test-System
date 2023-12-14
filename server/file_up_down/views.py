import os

from django.db.models import Max
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from file_up_down.forms import FileForm
from .models import PhtotDataModel
#from database_opt.models import DatabaseModel
from TestSystemServer.settings import BASE_DIR
import zipfile
import tempfile
from wsgiref.util import FileWrapper
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import time

STATIC_IMG_FILES_DIR = os.path.join(BASE_DIR, 'static/static')


# 解压文件
def unZipFile(unZipSrc, targeDir, filename, file):
    # if not os.path.isfile(unZipSrc):
    # raise Exception,u'unZipSrc not exists:{0}'.format(unZipSrc)

    targeDir_temp = os.path.join(targeDir, filename)

    print(u'开始解压缩文件:{0}'.format(unZipSrc))

    unZf = zipfile.ZipFile(unZipSrc, 'r')

    flag = False
    for fileM in unZf.namelist():
        # if ('/' in fileM):
        if os.path.split(fileM)[0] != '':
            flag = True
            break

    if flag:
        for fileM in unZf.namelist():
            if not fileM.endswith("/"):
                unZf.extract(fileM, targeDir)
        unZipSrc_temp = os.path.join(targeDir, file)
        os.rename(unZipSrc_temp, targeDir_temp)
    else:
        if not os.path.exists(targeDir_temp):
            os.makedirs(targeDir_temp)
        for fileM in unZf.namelist():
            unZf.extract(fileM, targeDir_temp)

    print(u'解压缩完毕，目标文件目录:{0}'.format(targeDir_temp))

    unZf.close()

    """
    for name in unZf.namelist() :
        unZfTarge = os.path.join(targeDir,name)



        if not unZfTarge.endswith("/"):

            #empty dir
            splitDir = unZfTarge[:-1]
            if not os.path.exists(splitDir):
                os.makedirs(splitDir)
        else:

            splitDir,_ = os.path.split(targeDir)

            if not os.path.exists(splitDir):
                os.makedirs(splitDir)

            hFile = open(unZfTarge,'wb')
            hFile.write(unZf.read(name))
            hFile.close()
"""



# 上传文件之后，注册数据库
def register_db(user_querydict, path, filename, file_desc):


    # 若当前数据库中没有数据，则max_file_id设置为0
    data_count = PhtotDataModel.objects.count()
    if(data_count==0):
        max_file_id = 0
    else:
        # 获取当前数据库中最大的file_id
        max_file_id = PhtotDataModel.objects.aggregate(max_file_id=Max('file_id'))['max_file_id']

    print('-----------------------------------------------------------max_file_id')
    print(max_file_id)

    user_id = user_querydict.get('user_id', "")
    user_id = int(user_id)
    print('user_id---------------------------------------------')
    print(user_id)

    file_type = user_querydict.get('file_type', "")
    file_type = int(file_type)
    print('file_type---------------------------------------------')
    print(file_type)

    print('path---------------------------------------------')
    print(path)
    obj = PhtotDataModel(file_id=max_file_id+1, user_id=user_id, file_name=filename, file_type=file_type,
                         file_state='raw',file_desc=file_desc, file_path=path)
    obj.save()

    print('register database succeed!')

# test
@csrf_exempt
def test_view(request):
    return HttpResponse('上传成功!')

# 获取指定用户、指定file_type的所有文件
@csrf_exempt
def get_type_file_list(request):
    content = {"status": 0, "msg": "ok", "data": {"count": 0, "rows": []}}
    if request.method == 'GET':
        user_id = request.GET.get('userid', "")
        file_type = request.GET.get('filetype', "")
        dobjs = PhtotDataModel.objects.filter(user_id=int(user_id),file_type=file_type,file_state='raw')

        count = len(dobjs)
        content["data"]["count"] = count

        for idx, obj in enumerate(dobjs):
            print('----------------------------------------------obj')
            print(obj)
            mp_temp = {}

            mp_temp["label"] = 'File (id = ' + str(obj.file_id) + ')'
            mp_temp["value"] = obj.file_id

            content["data"]["rows"].append(mp_temp)

        return JsonResponse(content, safe=True)
    else:
        content = {"success": "0", "error": ""}
        return JsonResponse(content, safe=True)

# 获取所有文件
@csrf_exempt
def get_file_list(request):
    content = {"status": 0,"msg": "ok","data":{"count": 0,"rows": []}}

    if request.method == 'GET':
        userid = request.GET.get('userid', "")
        dobjs = PhtotDataModel.objects.filter(user_id=int(userid))
        print('----------------------------------------------dobjs')
        #print(dobjs[0].user_id)
        count = len(dobjs)
        content["data"]["count"] = count

        for idx, obj in enumerate(dobjs):
            print('----------------------------------------------obj')
            print(obj)
            mp_temp = {}

            mp_temp["file_id"] = obj.file_id
            mp_temp["user_id"] = obj.user_id
            mp_temp["file_name"] = obj.file_name
            mp_temp["file_type"] = obj.file_type
            mp_temp["file_state"] = obj.file_state
            mp_temp["file_desc"] = obj.file_desc
            mp_temp["file_path"] = obj.file_path
            mp_temp["upload_time"] = obj.upload_time
            content["data"]["rows"].append(mp_temp)


        return JsonResponse(content, safe=True)
    else:
        content = {"success": "0", "error": ""}
        return JsonResponse(content, safe=True)

# 将时间戳转换为'2023_06_15_11_54_54_222'这种形式
def timestamp_to_string(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]

# 上传文件
@csrf_exempt
def file_upload(request):
    """
    上传文件
    :param request: 文件压缩包+相关参数
    :return: null
    """
    if request.method == 'POST':

        form = FileForm(request.POST, request.FILES)
        # 如果目标目录还不存在，则进行创建
        upload_dir = os.path.join(STATIC_IMG_FILES_DIR, request.GET.get('user_id', ""))

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        if form.is_valid():
            # 选择的文件
            files = request.FILES.getlist('file')

            for file in files:
                # 写入到数据库中
                # file_model = FileModel(name=file.name, path=os.path.join(upload_dir, file.name))
                # file_model.save()

                # 写入到服务器本地
                destination = open(os.path.join(upload_dir, file.name), 'wb+')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()

                filename = file.name.replace('.zip', '')
                t = time.time()
                filename += '_'
                filename += timestamp_to_string(t)
                path = os.path.join(BASE_DIR, 'static/static', request.GET.get('user_id', ""), filename)
                # 需要解压的zip文件路径
                unZipSrc = os.path.join(os.path.join(BASE_DIR, 'static/static', request.GET.get('user_id', "")),file.name)
                # 解压目标文件夹路径
                targeDir = os.path.join(BASE_DIR, 'static/static', request.GET.get('user_id', ""))
                # 执行解压函数
                unZipFile(unZipSrc, targeDir, filename, file.name.replace('.zip', ''))
                # 删除zip文件
                os.remove(unZipSrc)
                # 注册数据库
                register_db(request.GET, path, filename, request.GET.get('file_desc', ""))

            content = {
                "status": 0,
                "msg": "文件上传成功！",

            }
            # 提示上传成功
            return JsonResponse(content, safe=True)


        else:
            content = {
                "status": 1,
                "msg": "文件格式有误，请重新上传！",
            }
            # 提示上传失败
            return JsonResponse(content, safe=True)
    else:
        content = {
            "status": 1,
            "msg": "文件上传失败！",
        }
        # 提示上传失败
        return JsonResponse(content, safe=True)


def zipdir(dirpath, name='aug.zip'):
    """
    Support directory compression up to two levels
    """
    zf = zipfile.ZipFile(os.path.join(dirpath, name), 'w')
    for ctx in os.listdir(dirpath):
        cur = os.path.join(dirpath, ctx)
        if os.path.isdir(cur):
            for f in os.listdir(cur):
                if f.endswith(".csv"):
                    filename = os.path.join(cur, f)
                    zipname = os.path.join(ctx, f)
                    print("zip file " + zipname)
                    zf.write(filename, arcname=zipname)
        else:
            if ctx.endswith(".csv"):
                print("zip file " + ctx)
                zf.write(ctx)

    zf.close()


def extract_results(dirpath):
    out = []
    for ctx in os.listdir(dirpath):
        cur = os.path.join(dirpath, ctx)
        if os.path.isdir(cur):
            for f in os.listdir(cur):
                if f.endswith(".csv"):
                    filename = os.path.join(cur, f)
                    zipname = os.path.join(ctx, f)
                    out.append({'name': zipname, 'filepath': filename})
        """
        else:
            if ctx.endswith(".csv"):
                out.append({'name':ctx, 'filepath':cur})
        """

    return out


