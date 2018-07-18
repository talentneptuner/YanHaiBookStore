from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, verbose_name="用户名",  unique=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), null=True, blank=True, verbose_name="性别",
                              max_length=8, default='male')
    tel = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    paypass = models.CharField(max_length=257,null=True,blank=True,verbose_name="支付密码")
    wallet = models.FloatField(default=500, verbose_name="账户余额")

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname

    def messagenums(self):
        return self.usermessage_set.filter(have_read=0).count()


class EmailCode(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=30, verbose_name="发送对象")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")
    send_type = models.CharField(choices=(('register', '注册'),('forgetpwd','忘记密码'),('modifyemail','修改邮箱'),('modifypaypwd','修改支付密码')), verbose_name="用途", max_length=20)

    class Meta:
        verbose_name = "邮箱验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}+{}'.format(self.email, self.get_send_type_display())

class Address(models.Model):
    province = models.CharField(max_length=30,verbose_name="省")
    city = models.CharField(max_length=30,verbose_name="市")
    region = models.CharField(max_length=30,verbose_name="区/县",null=True,blank=True)
    town = models.CharField(max_length=40,verbose_name="乡镇/街道",null=True,blank=True)
    detail = models.CharField(max_length=200,verbose_name="具体地址")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="加入时间")
    name = models.CharField(max_length=20,verbose_name="联系人姓名")
    tel = models.CharField(max_length=11,verbose_name="联系方式")
    user = models.ForeignKey(UserProfile,verbose_name="所属用户",on_delete=models.CASCADE)

    class Meta:
        verbose_name="地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}{}{}{}{}".format(self.province,self.city,self.region,self.town,self.detail)

    def get_display(self):
        if self.town:
            return "{}{}{}{}{}  {}  {}".format(self.province,self.city,self.region,self.town,self.detail,self.name,self.tel)
        else:
            return "{}{}{}{}  {}  {}".format(self.province, self.city, self.region, self.detail, self.name,
                                               self.tel)
