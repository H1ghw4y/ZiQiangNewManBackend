from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import ShopSerializer


class ShopView(APIView):
    # 获取数据
    def get(self, request):
        is_sort = request.query_params.get('sort')
        is_selection = request.query_params.get('selection')
        # page、pagesize还未使用
        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')
        # print("is_sort=",is_sort)
        # print(type(is_sort))
        # data = models.Shop.objects.all()
        # info = ShopSerializer(data, many=True)
        # print("lllll")
        if is_selection == "True":
            # 这里is_sort是str, 默认是按shop_score排序，为True才按comment_count排序
            if is_sort == "True":
                data = models.Shop.objects.filter(shop_isChiHu=True).order_by('-comment_count')
            else:
                data = models.Shop.objects.filter(shop_isChiHu=True).order_by('-shop_score')
            shop_count = models.Shop.objects.filter(shop_isChiHu=True).count()
        else:
            if is_sort == "True":
                data = models.Shop.objects.all().order_by('-comment_count')
            else:
                data = models.Shop.objects.all().order_by('-shop_score')
            shop_count = models.Shop.objects.all().count()
        info = ShopSerializer(data, many=True)
        return Response({
            "status": 200,
            "msg": "",
            "count": shop_count,
            "data": info.data
        })

    # 添加数据
    def post(self, request):
        data = request.data
        flag = models.Shop.objects.create(**data)
        if not flag:
            return Response({
                "status": 201,
                "msg": "学生添加失败",
                "data": []
            })
        return Response({
            "status": 200,
            "msg": "学生添加成功",
            "data": []
        })

    # 编辑数据
    def put(self, request):
        id = request.data.pop('id')
        flag = models.Shop.objects.filter(id=id).update(**request.data)
        if not flag:
            return Response({
                "status": 201,
                "msg": "数据编辑失败",
                "data": []
            })
        return Response({
            "status": 200,
            "msg": "数据编辑成功",
            "data": []
        })

    # 删除数据
    def delete(self, request):
        id = request.data.get('id')
        student = models.Shop.objects.filter(id=id).delete()
        if not student[0]:
            return Response({
                "status": 201,
                "msg": "删除失败",
                "data": []
            })
        return Response({
            "status": 200,
            "msg": "删除成功",
            "data": []
        })
