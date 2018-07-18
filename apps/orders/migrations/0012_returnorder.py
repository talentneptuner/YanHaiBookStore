# Generated by Django 2.0.2 on 2018-06-02 19:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20180602_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnOrder',
            fields=[
                ('id', models.CharField(max_length=26, primary_key=True, serialize=False, verbose_name='退货单号')),
                ('type', models.CharField(choices=[('m', '退款'), ('mc', '退货与款')], default='mc', max_length=4, verbose_name='退单类型')),
                ('reason', models.CharField(blank=True, max_length=200, null=True, verbose_name='原因')),
                ('status', models.CharField(blank=True, choices=[('un', '未退回'), ('ing', '退回中'), ('ed', '已退回')], max_length=10, null=True, verbose_name='退货状态')),
                ('tracking', models.CharField(blank=True, max_length=20, null=True, verbose_name='快递单号')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.DeliveryOrder', verbose_name='对应出货单')),
            ],
            options={
                'verbose_name': '退货单',
                'verbose_name_plural': '退货单',
            },
        ),
    ]