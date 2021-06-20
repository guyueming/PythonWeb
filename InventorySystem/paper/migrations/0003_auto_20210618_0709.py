# Generated by Django 3.2.3 on 2021-06-17 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0002_papermodel_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='papermodel',
            name='factory',
            field=models.TextField(default='', max_length=64, verbose_name='厂家'),
        ),
        migrations.AlterField(
            model_name='papermodel',
            name='type',
            field=models.TextField(default='', max_length=64, verbose_name='型号'),
        ),
    ]
