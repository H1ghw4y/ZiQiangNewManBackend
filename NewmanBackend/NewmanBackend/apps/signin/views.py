from django.http import JsonResponse, HttpResponse
from db.models import User
import json

# def signin(request):
#     # models.Book.objects.create(title='三国演义',price=100)
#     dic = {"sid":2022,"password":123}
#     User.objects.create(**dic)
#     return HttpResponse('OK')

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
