from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from ..db.models import Collect, Shop, User
from .serializers import ShopSerializer


def get(request):
    sid = request.GET.get('sid')
    is_sort = request.GET.get('sort')
    is_selection = request.GET.get('selection')
    user = User.objects.get(sid=sid)
    id = user.id
    my_collect = Collect.objects.filter(user_id=id).order_by('-time').values_list("shop_id", flat=True)
    # shops=Shop.objects.filter(id=my_collect[0])
    # for a in my_collect[1:]:
    #     shops+=Shop.objects.filter(id=a)
    shops = Shop.objects.filter(id__in=my_collect)
    # for a in my_collect:
    #     print(a)
    #print(shops)
    if is_selection == "True":
        # 这里is_sort是str, 默认是按shop_score排序，为True才按time排序
        if is_sort == "True":
            data = shops.filter(shop_isChiHu=True).order_by('-shop_score')
            shop_count = data.count()
            info1 = ShopSerializer(data, many=True)
            info = info1.data
            print(info)
        else:
            data1 = shops.filter(shop_isChiHu=True)
            shop_count = data1.count()
            print(data1)
            info = []
            for c in my_collect:
                print(c)
                try:
                    print('5')
                    shop = data1.get(id=c)
                    info1 = ShopSerializer(shop)
                    print('0')
                    print(info1.data)
                    info.append(info1.data)
                    print('6')
                except:
                    print('7')
            print(info)
    else:
        if is_sort == "True":
            data = shops.order_by('-shop_score')
            shop_count = data.count()
            info1 = ShopSerializer(data, many=True)
            info = info1.data
        else:
            data1 = shops
            shop_count = data1.count()
            info = []
            for c in my_collect:
                try:
                    shop = data1.get(id=c)
                    info1 = ShopSerializer(shop)
                    info.append(info1.data)
                except:
                    pass
    return JsonResponse({
        "status": 200,
        "msg": "",
        "count": shop_count,
        "data": info
    })


def search(request):
    shop_name = request.GET.get("shop_name")
    try:
        shop = Shop.objects.get(shop_name=shop_name)
        shop_id = shop.id
    except:
        return JsonResponse('don\'t exist', safe=False)
    try:
        shop_exist = Collect.objects.get(shop_id=shop_id)
        info = ShopSerializer(shop)
        return JsonResponse(info.data)
    except:
        return JsonResponse('don\'t exist', safe=False)
