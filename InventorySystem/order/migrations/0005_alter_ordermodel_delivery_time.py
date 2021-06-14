# Generated by Django 3.2.3 on 2021-06-14 17:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_ordermodel_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='delivery_time',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='交货时间'),
        ),
    ]
