# Generated by Django 3.2.3 on 2021-06-17 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skin', '0002_alter_skinmodel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='skinmodel',
            name='factory',
            field=models.TextField(default='', max_length=64, verbose_name='厂家'),
        ),
    ]