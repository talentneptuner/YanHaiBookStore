# Generated by Django 2.0.2 on 2018-06-02 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20180602_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logistics',
            name='id',
            field=models.CharField(max_length=26, primary_key=True, serialize=False, verbose_name='物流号'),
        ),
    ]
