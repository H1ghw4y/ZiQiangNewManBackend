from rest_framework import serializers
import sys

sys.path.append("..")
from db.models import User, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id', 'sid', 'password')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('shop',)
