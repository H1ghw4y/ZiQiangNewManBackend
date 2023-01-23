from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
import json
import sys

sys.path.append("..")
from db.models import Comment, Shop, User
from .serializers import ShopSerializer


class Todo(View):
    # 获取待认证店铺
    def get(self, request):
        user_is_ch_id = User.objects.filter(is_ch=True).values_list("id", flat=True)
        comments = Comment.objects.filter(user__in=user_is_ch_id).filter(shop_score=10).order_by('shop')
        shop_ids = comments.values_list("shop_id", flat=True)
        id_flat = 1
        i = 0
        ids = []  # 达到标准的店铺id
        todo_id = []  # 待认证的店铺id
        for shop_id in shop_ids:
            if shop_id == id_flat:
                i += 1
            else:
                if i >= 3:
                    ids.append(id_flat)
                i = 1
        for id in ids:
            shop = Shop.objects.get(id=id)
            if shop.shop_isChiHu == False:
                todo_id.append(id)
        todo_shops = Shop.objects.filter(id__in=todo_id)
        count = todo_shops.count()
        todo = ShopSerializer(todo_shops, many=True)
        data = todo.data
        return JsonResponse({
            "count": count,
            "data": data
        }, safe=False)

    # 认证店铺
    def post(self, request):
        data = json.loads(request.body)
        shop_id = data.get('shop_id')
        shop = Shop.objects.get(id=shop_id)
        shop.shop_isChiHu = True
        shop.save()
        return JsonResponse({
            "status": 200,
            "msg": "认证成功",
        }, safe=False)
