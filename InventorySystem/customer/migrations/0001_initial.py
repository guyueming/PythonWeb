# Generated by Django 3.2.3 on 2021-06-02 17:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=64, verbose_name='名称')),
                ('address', models.TextField(max_length=64, verbose_name='地址')),
                ('phone', models.TextField(max_length=64, verbose_name='电话')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否禁用')),
                ('note', models.TextField(max_length=256, verbose_name='备注')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
            ],
        ),
    ]
