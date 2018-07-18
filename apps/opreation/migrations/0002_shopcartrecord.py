# Generated by Django 2.0.2 on 2018-05-09 15:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commoditys', '0007_commodity_sell_nums'),
        ('opreation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCartRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nums', models.IntegerField(verbose_name='数量')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commoditys.Commodity', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车记录',
                'verbose_name_plural': '购物车记录',
            },
        ),
    ]
