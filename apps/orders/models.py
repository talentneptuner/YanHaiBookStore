from datetime import datetime
from django.db import models

from users.models import UserProfile
from commoditys.models import Commodity
from users.models import Address
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Order(models.Model):
    id = models.CharField(max_length=25, verbose_name="订单编号", primary_key=True)
    user = models.ForeignKey(UserProfile, verbose_name="下单用户", on_delete=models.CASCADE)
    status = models.CharField(choices=(('unpaid', '未付款'), ('paid', '已支付'), ('fininshed', '已完成')), max_length=11,
                              verbose_name="订单状态");
    total_price = models.FloatField(verbose_name="订单总价")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def get_delivery(self):
        return self.deliveryorder_set.all()

    def __str__(self):
        return self.id

    def isallout(self):
        for delivery in self.get_delivery().all():
            if delivery.status == 'ing':
                return False
        return True

    def allreturn(self):
        result = 1
        for de in self.deliveryorder_set.all():
            if not de.returnorder_set.all().count() == 0:
                result = 0
        return result


class DeliveryOrder(models.Model):
    id = models.CharField(max_length=26, verbose_name="出货单号", primary_key=True)
    address = models.CharField(max_length=200, verbose_name="收货信息", null=True, blank=True)
    order = models.ForeignKey(Order, verbose_name="所属订单", on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, verbose_name="商品", on_delete=models.CASCADE)
    nums = models.IntegerField(default=1, verbose_name="购买数量")
    status = models.CharField(choices=(('ing', '出货中'), ('ed', '已出货')), max_length=5, verbose_name="出货情况")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name_plural = "出货单"
        verbose_name = verbose_name_plural

    def get_totalprice(self):
        return self.commodity.price * self.nums

    def __str__(self):
        return self.id

    def is_out(self):
        if self.logistics_set.all():
            return True
        else:
            return False

    def mytracking_nums(self):
        return self.logistics_set.all()[0].track_nums

    def is_re(self):
        if self.returnorder_set.all():
            return 1
        else:
            return 0





class Logistics(models.Model):
    id = models.CharField(max_length=26, verbose_name="物流号", primary_key=True)
    Company = models.CharField(max_length=20, verbose_name="快递企业", default='顺丰')
    reciever = models.CharField(max_length=20, verbose_name='取件人')
    track_nums = models.CharField(max_length=20, verbose_name='快递单号', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    delivery = models.ForeignKey(DeliveryOrder, verbose_name='对应出货单', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '物流单'
        verbose_name = '物流单'

    def __str__(self):
        return self.id


class ReturnOrder(models.Model):
    id = models.CharField(max_length=26, verbose_name="退货单号", primary_key=True)
    type = models.CharField(max_length=4,choices=(('m','退款'),('mc','退货与款')),default='mc',verbose_name='退单类型')
    status = models.CharField(max_length=10,choices=(('ing','审核中'),('accept','同意退款'),('reject','拒绝退款')),verbose_name='状态',default='ing')
    reason = models.CharField(max_length=200,verbose_name='原因',null=True,blank=True)
    re_status = models.CharField(max_length=10,choices=(('un','未退回'),('ing','退回中'),('ed','已退回')),verbose_name='退货状态',default='un',null=True,blank=True)
    tracking = models.CharField(max_length=20,verbose_name='快递单号',null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    delivery = models.ForeignKey(DeliveryOrder, verbose_name='对应出货单', on_delete=models.CASCADE)
    finish = models.BooleanField(verbose_name='是否完成',default=False)

    class Meta:
        verbose_name = '退货单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

    def desc(self):
        return '{},{},{},{},{}'.format(self.delivery.order.user,self.delivery.commodity,self.delivery.get_totalprice(),self.delivery.get_status_display(),self.delivery.order.get_status_display())

    desc.short_description = '出货情况'




