# Generated by Django 2.0.2 on 2018-06-02 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20180602_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnorder',
            name='status',
            field=models.CharField(choices=[('accept', '同意退货'), ('reject', '拒绝退款'), ('ing', '审核中')], default='ing', max_length=7, verbose_name='退货审核'),
        ),
    ]
