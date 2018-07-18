from datetime import datetime

from django.db import models
from users.models import UserProfile
from commoditys.models import Commodity
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class LackCommodity(models.Model):

    name = models.CharField(max_length=50,verbose_name="书名")
    url = models.CharField(max_length=100,verbose_name="链接")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="填写时间")
    user = models.ForeignKey(UserProfile,verbose_name="登记用户",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "缺货登记"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ShopCartRecord(models.Model):

    user = models.ForeignKey(UserProfile,verbose_name="用户",on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity,verbose_name="商品",on_delete=models.CASCADE)
    nums = models.IntegerField(verbose_name="数量")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "购物车记录"
        verbose_name_plural = "购物车记录"

    def get_price(self):
        return self.nums*self.commodity.price


class UserMessage(models.Model):

    user = models.ForeignKey(UserProfile,verbose_name="发送对象",on_delete=models.CASCADE)
    content = models.CharField(max_length=500,verbose_name="信息内容")
    have_read = models.BooleanField(default=False,verbose_name="是否已读")
    send_time = models.DateTimeField(default=datetime.now,verbose_name="发送时间")

    class Meta:
        verbose_name_plural = "信息"
        verbose_name = verbose_name_plural

    def __str__(self):
        return "{}/{}".format(self.user.nickname,self.send_time)


class UserComment(models.Model):
    rank = models.IntegerField(verbose_name="评分")
    content = models.CharField(max_length=500,verbose_name="内容")
    user = models.ForeignKey(UserProfile,verbose_name="用户",on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity,verbose_name="商品",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now,verbose_name="评论时间")
    is_anon = models.BooleanField(default=False,verbose_name="是否匿名")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = "用户评论"

    def __str__(self):
        return "{}/{}".format(self.user.nickname,self.commodity.name)

