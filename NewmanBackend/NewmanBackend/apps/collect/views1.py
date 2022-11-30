from django.http import JsonResponse

import sys

sys.path.append("..")
from db.models import Comment, User, Shop
from user.serializers import *


def get(request):
    sid = request.GET.get('sid')
    user1 = User.objects.get(sid=sid)
    user = UserSerializer(user1)
    comments = Comment.objects.filter(user=user1.id).order_by("-id")
    response_data = dict()
    response_data['user'] = user.data
    response_data["comment_count"] = comments.count()
    response_data["comment"] = list()
    for comment in comments:
        item = parse2object(comment)
        response_data["comment"].append(item)
    return JsonResponse(response_data)


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
    the_user = User.objects.get(id=comment.user)
    data["time"] = comment.publish_time.strftime("%Y-%m-%d")
    data["user_name"] = the_user.user_name
    data["user_profile_photo_url"] = the_user.image
    # 你要修改好图片路径，才能使用下面的代码
    # try:
    #     photos = models.Photos.objects.get(id=comment.id)
    #     for photo in photos:
    #         user_dict["image_url"].append(photo.image)
    # except models.Photos.DoesNotExist:
    #     pass
    the_shop = Shop.objects.get(id=comment.shop)
    data['shop_name'] = the_shop.shop_name
    data["comment_id"] = str(comment.id)
    data["comment_content"] = comment.comment_content
    data["comment_like_count"] = comment.like_count
    data["comment_review_count"] = comment.reply_count
    return data
