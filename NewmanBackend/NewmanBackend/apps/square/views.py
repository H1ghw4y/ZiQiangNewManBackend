from django.http import JsonResponse
from django.shortcuts import render

# from NewmanBackend.NewmanBackend.apps.shop.models import Shop
import sys

sys.path.append("..")
from shop.models import Shop
# Create your views here.
from .models import Comment, User


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
    new_comments = comments[query_start:query_start + data_count]
    response_data = dict()
    response_data["data_count"] = data_count
    response_data["data"] = list()
    for comment in new_comments:
        item = parse2object(comment)
        response_data["data"].append(item)
    return JsonResponse(response_data)


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
    try:
        the_user = User.objects.get(id=comment.user_id)
    except User.DoesNotExist:
        pass
    user_dict = dict()
    shop_dict = dict()
    user_dict["time"] = comment.publish_time.strftime("%Y-%m-%d")
    user_dict["user_name"] = the_user.username
    # user_dict["user_profile_photo_url"] = the_user.user_profile_photo
    user_dict["is_ChiHu"] = str(the_user.is_chihu)
    user_dict["image_url"] = list()
    # try:
    #     photos = models.Photos.objects.get(id=comment.id)
    #     for photo in photos:
    #         user_dict["image_url"].append(photo.image)
    # except models.Photos.DoesNotExist:
    #     pass
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
