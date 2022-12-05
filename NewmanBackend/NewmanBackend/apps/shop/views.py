from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShopSerializer
import sys

sys.path.append("..")
from db.models import Comment, Shop
from square.serializers import CommentSerializer

class ShopView(APIView):
    # 获取数据
    def get(self, request):
        is_sort = request.query_params.get('sort')
        is_selection = request.query_params.get('selection')
        # page、pagesize还未使用
        page = int(request.query_params.get('page'))
        page_size = int(request.query_params.get('page_size'))
        # print("is_sort=",is_sort)
        # print(type(is_sort))
        # data = models.Shop.objects.all()
        # info = ShopSerializer(data, many=True)
        # print("lllll")
        if is_selection == "True":
            # 这里is_sort是str, 默认是按shop_score排序，为True才按comment_count排序
            if is_sort == "True":
                data = Shop.objects.filter(shop_isChiHu=True).order_by('-comment_count')[:page*page_size]
            else:
                data = Shop.objects.filter(shop_isChiHu=True).order_by('-shop_score')[:page*page_size]
            shop_count = Shop.objects.filter(shop_isChiHu=True)[:page*page_size].count()
        else:
            if is_sort == "True":
                data = Shop.objects.all().order_by('-comment_count')[:page*page_size]
            else:
                data = Shop.objects.all().order_by('-shop_score')[:page*page_size]
            shop_count = Shop.objects.all()[:page*page_size].count()
        info = ShopSerializer(data, many=True)
        return Response({
            "count": shop_count,
            "data": info.data
        })

    # 由于暂时没有考虑商家入驻，post,put,delete等方法未实现
    # 添加数据
    def post(self, request):
        data = request.data
        flag = Shop.objects.create(**data)
        if not flag:
            return Response({
                "status": 201,
                "msg": "添加失败",
                "data": []
            })
        return Response({
            "status": 200,
            "msg": "添加成功",
            "data": []
        })

    # 编辑数据
    def put(self, request):
        id = request.data.pop('id')
        flag = Shop.objects.filter(id=id).update(**request.data)
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
        student = Shop.objects.filter(id=id).delete()
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


# 商铺详情,参数参考之前在QQ群里发的models.py
# is_mark还未实现 2022-11-28

class ShopDetailView(APIView):
    def get(self, request):
        page = int(request.query_params.get('page'))
        page_size = int(request.query_params.get('page_size'))
        the_shop_name = request.query_params.get('shop_name')
        is_sort = request.query_params.get('sort')
        official_evaluation = request.query_params.get('official_evaluation')
        is_mark = request.query_params.get('mark')
        # 只查看吃乎作者的评价
        if official_evaluation == "True":
            if is_sort == "True":
                # 按时间排序
                data = Comment.objects.filter(shop__shop_name=the_shop_name, user__is_ch=True).order_by('-publish_time')[:page*page_size]
<<<<<<< HEAD

=======
>>>>>>> ZJY
            else:
                data = Comment.objects.filter(shop__shop_name=the_shop_name, user__is_ch=True).order_by('-like_count')[:page*page_size]
            count = Comment.objects.filter(shop__shop_name=the_shop_name, user__is_ch=True)[:page*page_size].count()
        else:
            if is_sort == "True":
                # 按时间排序
                data = Comment.objects.filter(shop__shop_name=the_shop_name).order_by('-publish_time')[:page*page_size]
            else:
                data = Comment.objects.filter(shop__shop_name=the_shop_name).order_by('-like_count')[:page*page_size]
            count = Comment.objects.filter(shop__shop_name=the_shop_name)[:page*page_size].count()
        info = CommentSerializer(data, many=True)
        return Response({
            "count": count,  # 还没写
            "data": info.data
        })
