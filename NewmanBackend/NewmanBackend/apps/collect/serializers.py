from rest_framework import serializers
from ..db import models


# shop数据序列化
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        exclude = ('is_delete',)
