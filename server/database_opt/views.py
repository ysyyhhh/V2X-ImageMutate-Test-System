from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from configure.paths import CONFIG_DIR
from django.views.decorators.csrf import csrf_exempt
from common.modelValidation import ModelValidation
from configure.paths import CONFIG_DIR, MEDIA_DIR
from .models import DatabaseModel
import os
import json
import shutil

# Create your views here.
def register_db(request):
    content = {"success": "0", "error": ""}
    if request.method == "GET":
        # * get userid
        userid = request.GET.get('userid', "")
        if userid == "":
            content["success"] = "-1"
            content["error"] = "userid error"
            return JsonResponse(content, safe=True)
        userid = int(userid)

        # * get path of the database
        path = request.GET.get('path', "")
        if path == "":
            content["success"] = "-1"
            content["error"] = "path is empty"
            return JsonResponse(content, safe=True)

        name = request.GET.get('name', "")
        desc = request.GET.get('desc', "")

        obj = DatabaseModel(idx=userid, name=name, desc=desc, path=path)
        obj.save()

    return JsonResponse(content, safe=False)

@csrf_exempt
def remove_db(request):
    content = {"success": "0", "error": ""}
    if request.method == "POST":
        # * get userid
        userid = request.POST.get('userid', "")
        if userid == "":
            content["success"] = "-1"
            content["error"] = "userid error"
            return JsonResponse(content, safe=True)
        userid = int(userid)

        # * get path of the database
        path = request.POST.get('path', "")
        if path == "":
            content["success"] = "-1"
            content["error"] = "path is empty"
            return JsonResponse(content, safe=True)

        name = request.POST.get('name', "")
        desc = request.POST.get('desc', "")

        DatabaseModel.objects.filter(idx=userid, path=path).delete()

        # * do post process
        tgt = os.path.join(path, "processed")
        if os.path.exists(tgt):
            shutil.rmtree(tgt)

    return JsonResponse(content, safe=False)

def get_db(request):
    content = {"success": "0", "error": "", "db": {}}
    if request.method == "GET":
        # * get userid
        userid = request.GET.get('userid', "")
        if userid == "":
            content["success"] = "-1"
            content["error"] = "userid error"
            return JsonResponse(content, safe=True)
        userid = int(userid)

        # * get path of the database

        objs = DatabaseModel.objects.filter(idx=userid)

        for idx, d in enumerate(objs):
            content["db"][str(idx+1)] = {"name": d.name, "desc": d.desc, "path": d.path}

    return JsonResponse(content, safe=False)
