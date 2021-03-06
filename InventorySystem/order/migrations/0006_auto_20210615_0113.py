# Generated by Django 3.2.3 on 2021-06-14 17:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_ordermodel_delivery_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperformmodel',
            name='arrive_time',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='到货时间'),
        ),
        migrations.AlterField(
            model_name='skinformmodel',
            name='arrive_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='到货时间'),
        ),
        migrations.AlterField(
            model_name='woodformmodel',
            name='arrive_time',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='到货时间'),
        ),
    ]
