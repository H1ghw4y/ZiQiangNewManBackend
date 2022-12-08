from django.db import models

# Create your models here.
from django.db import models

#
# class Shop(models.Model):
#     shop_name = models.CharField(max_length=20, verbose_name='店铺名称')
#     # upload_to 指定的路径待定
#     shop_profile_photo = models.ImageField(upload_to='photos', verbose_name='店铺图片', null=True)
#     shop_score = models.IntegerField(default=0, verbose_name='店铺评分')
#     comment_count = models.IntegerField(default=0, verbose_name='评论量')
#     shop_isChiHu = models.BooleanField(default=False, verbose_name='是否吃乎认证')
#     # 注销该店铺
#     is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
#
#     class Meta:
#         # 指定表名
#         db_table = 'Shops'
#         verbose_name = '店铺'  # 在admin站点中显示的名称
#         verbose_name_plural = verbose_name  # 显示的复数名称
#
#     def __str__(self):
#         """定义每个数据对象的显示信息"""
#         return self.shop_name
