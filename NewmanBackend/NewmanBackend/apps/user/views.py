import json
from .serializers import *

from django.http import JsonResponse, QueryDict
import sys

sys.path.append("..")
from db.models import *
from django.views.generic import View
from .serializers import *


def get(request):
    sid = request.GET.get('sid')
    user1 = User.objects.get(sid=sid)
    user = UserSerializer(user1)
    try:
        image = user1.image.url
    except:
        image = "/media/photos_user/默认头像.jpg"
    comments = Comment.objects.filter(user=user1.id).order_by("-id")
    response_data = dict()
    response_data['user_data'] = user.data
    response_data['user_data']['image'] = image
    response_data["comment_count"] = comments.count()
    response_data["comment"] = list()
    for comment in comments:
        item = parse2object(comment)
        response_data["comment"].append(item)
    return JsonResponse(response_data, safe=False)


# ----------------------------utils-----------------------------------
def parse2object(comment: Comment):
    """
    "comment": {
        "time": "2021-11-17",
        "user_name": "Tom",
        "user_profile_photo_url": "image_url",
        "comment_id": "001",
        "shop_name": "工学部小吃"
        "comment_content": "xxxx",
        "comment_like_count": 12,
        "comment_review_count": 13
        "image_url": [
            "iamge1_url",
            "image2_url",
            "iamge3_url"
            ]
        }
    """
    data = dict()
    the_user = User.objects.get(id=comment.user_id)
    data["time"] = comment.publish_time.strftime("%Y-%m-%d")
    data["user_name"] = the_user.user_name
    data["image_url"] = list()
    # 评论图片
    try:
        photos = Photos.objects.filter(id=comment.id)
        for photo in photos:
            data["image_url"].append(photo.image.url)
    except:
        pass
    the_shop = Shop.objects.get(id=comment.shop_id)
    data['shop_name'] = the_shop.shop_name
    data["comment_score"] = comment.shop_score
    data["comment_id"] = str(comment.id)
    data["comment_content"] = comment.comment_content
    data["comment_like_count"] = comment.like_count
    data["comment_review_count"] = comment.reply_count
    return data


def change_tx(request):
    params: QueryDict = request.POST
    sid = params.get("sid")
    image = request.FILES.get("tx_photo")
    user = User.objects.get(sid=sid)
    user.image = image
    user.save()
    return JsonResponse({'image': user.image.url})


def change_name(request):
    data = json.loads(request.body)
    sid = data.get('sid')
    user_name = data.get('user_name')
    user = User.objects.get(sid=sid)
    user.user_name = user_name
    user.save()
    return JsonResponse({'user_name': user_name})


class Renzheng(View):

    # 查询是否为吃乎用户
    def get(self, request):
        a = {'is1': True}
        sid = request.GET.get('sid')
        user = User.objects.get(sid=sid)
        if user.is_ch == True:
            return JsonResponse(a)
        else:
            a['is1'] = False
            return JsonResponse(a)

    # 认证吃乎用户
    def post(self, request):
        b = {'is2': True}
        data = json.loads(request.body)
        id = data.get('id')
        user = User.objects.get(sid=id)
        ch = Chihu.objects.all()
        for ch_user in ch:
            if ch_user.user_id == id:
                user.is_ch = True
                user.save()
                return JsonResponse(b)
        b['is2'] = False
        return JsonResponse(b)
