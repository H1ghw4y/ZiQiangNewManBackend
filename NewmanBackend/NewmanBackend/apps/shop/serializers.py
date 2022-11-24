from rest_framework import serializers
from . import models

# shop数据序列化
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = '__all__'