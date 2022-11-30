from rest_framework import serializers
import sys

sys.path.append("..")
from db.models import Comment


# shop数据序列化
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
