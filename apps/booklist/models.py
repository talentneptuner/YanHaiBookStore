from django.db import models
from datetime import datetime
# Create your models here.
from commoditys.models import Commodity
from users.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator


class BookList(models.Model):
    title = models.CharField(max_length=30, verbose_name='标题')
    tag1 = models.CharField(max_length=30, verbose_name='标签一')
    tag2 = models.CharField(max_length=30, verbose_name='标签二',null=True,blank=True)
    click_nums = models.IntegerField(verbose_name='点击量',default=0)
    desc = models.CharField(max_length=500, verbose_name='简介',null=True,blank=True)
    is_pub = models.BooleanField(verbose_name='是否公开',default=True)
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='booklist/%Y/%m',verbose_name="封面",null=True,blank=True)
    add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now,null=True,blank=True)
    fav_nums = models.IntegerField(verbose_name='收藏',default=0)
    book_nums = models.IntegerField(verbose_name='书籍数',default=0)

    class Meta:
        verbose_name_plural = '书单'
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.title

    def set_favnums(self):
        self.fav_nums = self.userfav_set.all().count()

    def set_booknums(self):
        self.book_nums = self.booklistdetail_set.all().count()


class BookListDetail(models.Model):
    booklist = models.ForeignKey(BookList, verbose_name='书单', on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, verbose_name='商品', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now,null=True,blank=True)

    class Meta:
        verbose_name_plural = '书单记录'
        verbose_name = verbose_name_plural


class UserFav(models.Model):
    booklist = models.ForeignKey(BookList,verbose_name='书单',on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间',default=datetime.now,null=True,blank=True)

    class Meta:
        verbose_name_plural = '收藏书单'
        verbose_name = verbose_name_plural

