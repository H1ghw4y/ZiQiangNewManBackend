from django.http import JsonResponse, HttpResponse
import sys

sys.path.append("..")
from db.models import User
import json
import hashlib


def create_user(sid, password):
    # 2023-2-5: 改明码存储为哈希值存储
    hash_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    User.objects.create(
        sid=sid,
        password=hash_password
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
    hash_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if user.password == hash_password:
        if user.is_admin == True:
            a['is'] = 'true_admin'
        if user.is_admin == False:
            a['is'] = 'true_user'
    else:
        a['is'] = 'false'
    return JsonResponse(a)



