import datetime
import json
import random

from django.http import JsonResponse, HttpResponse, QueryDict

import sys

from django.shortcuts import render

sys.path.append("..")
from db.models import Shop, Comment, User, Huitie, PhotoHuiTie

try:
    from ..db.models import Shop, Comment, User, Huitie, PhotoHuiTie, Photos
except:
    pass


# Create your views here.

def api_test(request):
    # comments = Comment.objects.all()
    # for comment in comments:  # 对每个评论回复
    #     huitie_contents = [f"{i}" * 9 + f"->to comment_id{comment.id}" for i in range(1, 8)]  # 构造回帖内容,i为用户id
    #     for idx, Huitie_content in enumerate(huitie_contents):  # 模拟每个用户都评论
    #         uid = idx + 1
    #         if uid == comment.user.id:  # 自己不给自己回
    #             continue
    #         else:
    #             Huitie.objects.create(content=Huitie_content, user_id=uid, comment_id=comment.id)
    photo = PhotoHuiTie.objects.get(id=1)
    photos = photo.photos.url
    print(photos)
    return render(request, "1.html")


def get_page(request):
    """
    获取广场信息
    GET 参数
    page:
    page_size:
    """
    page_num = int(request.GET.get("page"))
    page_size = int(request.GET.get("page_size"))
    data_count = page_size
    query_start = page_num * page_size
    comments = Comment.objects.all().order_by("-publish_time")
    # 越界判断
    if query_start + data_count > comments.count() - 1:
        new_comments = comments[query_start:]
    else:
        new_comments = comments[query_start:query_start + data_count]
    response_data = dict()
    response_data["data_count"] = data_count
    response_data["data"] = list()
    for comment in new_comments:
        item = parse2object(comment)
        response_data["data"].append(item)
    return HttpResponse(
        json.dumps(response_data, ensure_ascii=False),
        content_type="application/json,charset=utf-8"
    )


def add_like(request):
    """用户点赞"""
    comment_id = int(request.GET.get("comment_id"))
    comment = Comment.objects.filter(id=comment_id)[0]
    comment.like_count += 1
    comment.save()
    return JsonResponse({"message": "True"})


def detail(request):
    """获取回帖
    {
  "data_count": 3,
  "data": [
    {
      "time": "2021-05-17",
      "user_name": "Sass",
      "user_profile_photo_url": "image_url",
      "comment": "xxx"
    },
    {
      "time": "2021-05-17",
      "user_name": "Sass",
      "user_profile_photo_url": "image_url",
      "comment": "xxx"
    },
    {
      "time": "2021-05-17",
      "user_name": "Sass",
      "user_profile_photo_url": "image_url",
      "comment": "xxx"
    }
  ]
}
    """

    GET_dict = request.GET
    comment_id = int(GET_dict.get("comment_id"))
    page = int(GET_dict.get("page"))
    page_size = int(GET_dict.get("page_size"))
    # 构造返回数据
    response_data = dict()
    response_data["data_count"] = page_size
    response_data["data"] = list()
    # 筛选回帖
    huitie_objects = Huitie.objects.filter(comment=comment_id).order_by("-date")
    start = page * page_size
    end = huitie_objects.count()
    # 越界判断
    if end - 1 <= start + page_size:
        huitie_objects = huitie_objects[start:]
    else:
        huitie_objects = huitie_objects[start:start + page_size]
    # 构造数据
    for huitie in huitie_objects:
        item = parse_detail(huitie)
        response_data["data"].append(item)
    return HttpResponse(
        json.dumps(response_data, ensure_ascii=False),
        content_type="application/json,charset=utf-8")


def publish(request):
    """发表评论"""
    if request.method == "GET":
        return render(request, "1.html")
    # 获取值
    params: QueryDict = request.POST
    comment_id = int(params.get("comment_id"))
    shop_id = int(params.get("shop_id"))
    user_id = int(params.get("user_id"))
    content = params.get("content")
    shop_score = int(params.get("shop_score"))
    # 数据库处理
    try:
        # 存储回帖图片
        image_list = request.FILES.getlist("photos")
        for image in image_list:
            print("@@@:", type(image))
            PhotoHuiTie.objects.create(comment_target_id=comment_id, photos=image)
    except Exception:
        print(Exception)
    # 评论+1
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.reply_count += 1
        comment.save()
    except:
        pass
    # 创建回帖数据
    Huitie.objects.create(user_id=user_id, comment_id=comment_id, content=content)
    # 对店铺评分
    try:
        shop = Shop.objects.get(id=shop_id)
        shop.shop_score += shop_score
        shop.comment_count += 1
        shop.save()
    except:
        pass
    return JsonResponse({"message": "True"})


# ----------------------------utils-----------------------------------
def parse2object(comment: Comment):
    """ "user": {
        "time": "2021-11-17",
        "user_name": "Tom",
        "user_profile_photo_url": "image_url",
        "is_ChiHu": "True",
        "comment": {
          "comment_id": "001",
          "comment_content": "xxxx",
          "comment_like_count": 12,
          "comment_review_count": 13
        },
        "image_url": [
          "iamge1_url",
          "image2_url",
          "iamge3_url"
        ]
      },
      "shop": {
        "shop_id": "str",
        "shop_name": "工学部小吃",
        "shop_score": 10
      }
    }"""
    data = dict()
    user = comment.user
    user_dict = dict()
    shop_dict = dict()

    user_dict["time"] = comment.publish_time.strftime("%Y-%m-%d")
    user_dict["user_name"] = user.user_name
    user_dict["user_profile_photo_url"] = ''
    try:
        user_dict["user_profile_photo_url"] = user.image.url
    except:
        pass
    user_dict["is_ChiHu"] = str(user.is_ch)
    user_dict["image_url"] = list()
    # 评论图片
    try:
        photos = Photos.objects.filter(id=comment.id)
        for photo in photos:
            user_dict["image_url"].append(photo.image.url)
    except:
        pass
    user_comment_dict = dict()
    user_comment_dict["comment_id"] = str(comment.id)
    user_comment_dict["comment_content"] = comment.comment_content
    user_comment_dict["comment_like_count"] = comment.like_count
    user_comment_dict["comment_review_count"] = comment.reply_count
    user_dict["comment"] = user_comment_dict
    try:
        the_shop = Shop.objects.get(id=comment.shop_id)
        shop_dict["shop_id"] = the_shop.id
        shop_dict["shop_name"] = the_shop.shop_name
        shop_dict["shop_score"] = comment.shop_score
        data["user"] = user_dict
        data["shop"] = shop_dict
    except Comment.DoesNotExist:
        pass
    return data


def parse_detail(huitie: Huitie):
    """{
      "time": "2021-05-17",
      "user_name": "Sass",
      "user_profile_photo_url": "image_url",
      "comment": "xxx"
    }"""
    data_dict = dict()
    user = huitie.user
    data_dict["time"] = huitie.date.strftime("%Y-%m-%d")
    data_dict[" user_name"] = user.user_name
    data_dict["user_profile_photo_url"] = user.image if user.image else ""
    data_dict["comment"] = huitie.content
    return data_dict
