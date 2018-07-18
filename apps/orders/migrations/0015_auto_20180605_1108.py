# Generated by Django 2.0.2 on 2018-06-05 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_returnorder_finish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnorder',
            name='re_status',
            field=models.CharField(blank=True, choices=[('un', '未退回'), ('ing', '退回中'), ('ed', '已退回')], default='un', max_length=10, null=True, verbose_name='退货状态'),
        ),
    ]