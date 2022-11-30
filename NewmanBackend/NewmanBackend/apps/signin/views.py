from django.http import JsonResponse, HttpResponse
import sys

sys.path.append("..")
from db.models import User
import json


def create_user(sid, password):
    User.objects.create(
        sid=sid,
        password=password
    )


def signin(request):
    data = json.loads(request.body)
    sid = data.get("sid")
    password = data.get("password")
    a = {'is': True}
    try:
        user = User.objects.get(sid=sid)
    except:
        create_user(sid, password)
        return JsonResponse(a)

    if user.password == password:
        pass
    else:
        a['is'] = False
    return JsonResponse(a)
