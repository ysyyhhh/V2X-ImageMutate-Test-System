from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def djregister(request):
    content = {"success": "-1", "error": "Please use POST method"}
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            User.objects.create_user(username=name, password=password)
            content['error'] = ""
            content['success'] = '0'
        except Exception as e:
            content['error'] = str(e)
            content['success'] = '-1'
    return JsonResponse(content)

@csrf_exempt
def djlogin(request):
    content = {"success": "-1", "error": "Please use POST method", "userid": ""}
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 验证用户名和密码，通过的话，返回User对象
        user = auth.authenticate(username=name, password=password)
        if user:
            auth.login(request, user)
            print("login success", request.session.get('_auth_user_id'))
            content['success'] = '0'
            content['error'] = ''
            content['userid'] = request.session.get('_auth_user_id')
        else:
            print("login fail")
            content['success'] = '-1'
            content['error'] = 'login fail'
            # return render(request, 'index.html')
    return JsonResponse(content)

def djlogout(request):
    content = {"success": "0", "error": ""}
    if request.method == 'GET':
        auth.logout(request)
        return JsonResponse(content)
