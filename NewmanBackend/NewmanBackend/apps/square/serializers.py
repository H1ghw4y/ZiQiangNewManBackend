from rest_framework import serializers
from . import models


# shop数据序列化
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'
