from rest_framework import serializers
import sys

sys.path.append("..")
from db.models import Shop

# shop数据序列化
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'