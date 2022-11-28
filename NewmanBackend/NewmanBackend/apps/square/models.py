from django.db import models


# from ..shop import *


# Create your models here.
# from ..shop.models import Shop


class User(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=20, verbose_name="用户名")
    user_account = models.CharField(max_length=15, verbose_name=" 用户账号")
    user_pwd = models.CharField(max_length=30, verbose_name="用户密码")
    user_profile_photo = models.ImageField(upload_to="photos/", verbose_name="用户头像", null=True)
    is_chihu = models.BooleanField(default=False, verbose_name="# 是否是吃乎作者")

    class Meta:
        db_table = "Users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_account + " " + self.username


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)  # 关联的
    shop = models.ForeignKey("shop.Shop", on_delete=models.CASCADE)  # 关联的店铺id
    comment_content = models.TextField(verbose_name="评论内容")
    publish_time = models.DateField(auto_now=True, verbose_name="发表时间")
    reply_count = models.IntegerField(verbose_name="回帖数量")
    like_count = models.IntegerField(verbose_name="点赞数量")
    shop_score = models.IntegerField(verbose_name="评论给店铺的分数")

    class Meta:
        db_table = "Comments"
        verbose_name = "评论表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class Photos(models.Model):
    """用于存放评论图片表"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photos/", verbose_name="评论的图片")

    class Meta:
        db_table = "Photos"
        verbose_name = "图片表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
