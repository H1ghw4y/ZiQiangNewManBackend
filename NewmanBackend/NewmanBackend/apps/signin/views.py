from django.http import JsonResponse, HttpResponse
import sys

sys.path.append("..")
from db.models import User
import json


def create_user(sid, password):
    User.objects.create(
        sid=sid,
        password=password,
        image="photos_user/默认头像.jpg"

    )


def signin(request):
    data = json.loads(request.body)
    sid = data.get("sid")
    password = data.get("password")
    a = {'is': 'true_user'}
    try:
        user = User.objects.get(sid=sid)
    except:
        create_user(sid, password)
        return JsonResponse(a)

    if user.password == password:
        if user.is_admin == True:
            a['is'] = 'true_admin'
        if user.is_admin == False:
            a['is'] = 'true_user'
    else:
        a['is'] = 'false'
    return JsonResponse(a)
