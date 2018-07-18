from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CatagoryF(models.Model):
    id = models.CharField(verbose_name="编号",primary_key=True,max_length=3)
    name = models.CharField(verbose_name="类别名", max_length=50)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "一级类别"
        verbose_name_plural = "一级类别"

    def __str__(self):
        return self.name


class CatagoryS(models.Model):
    id = models.CharField(max_length=5,verbose_name="编号",primary_key=True)
    name = models.CharField(verbose_name="类别名", max_length=50)
    cata_up = models.ForeignKey(CatagoryF, verbose_name="上级类别",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name_plural = "二级类别"
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.name


class CatagoryT(models.Model):
    id = models.CharField(verbose_name="编号",primary_key=True,max_length=7)
    name = models.CharField(verbose_name="类别名", max_length=50)
    cata_up = models.ForeignKey(CatagoryS, verbose_name="上级类别",on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "三级类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Commodity(models.Model):
    id = models.CharField(verbose_name="商品编号",max_length=15,primary_key=True)
    name = models.CharField(max_length=100, verbose_name="书名")
    price = models.FloatField(verbose_name="价格")
    author = models.CharField(verbose_name="作者", max_length=100, null=True, blank=True)
    publisher = models.CharField(verbose_name="出版社", max_length=100, null=True, blank=True)
    isbn = models.CharField(verbose_name="ISBN", max_length=20)
    stock = models.IntegerField(default=0, verbose_name="库存量")
    size = models.CharField(max_length=20,verbose_name="开本",default="16开",null=True,blank=True)
    pubdate = models.CharField(max_length=30,verbose_name="出版月份",default="2018年8月",null=True,blank=True)
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    desc = models.TextField(verbose_name="简述",null=True,blank=True)
    catalog = models.TextField(verbose_name="目录",null=True,blank=True)
    image = models.ImageField(verbose_name="图片", upload_to="commodity/%Y/%m")
    catagory = models.ForeignKey(CatagoryT,verbose_name="类别",null=True,blank=True,on_delete=models.SET_NULL)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    sell_nums = models.IntegerField(default=0,verbose_name="销量")
    is_sale = models.CharField(choices=(('in','在售'),('out','下架')),max_length=10,verbose_name='销售状态',default='in')

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
