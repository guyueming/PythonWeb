# Generated by Django 3.2.3 on 2021-06-17 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wood', '0002_woodmodel_surface'),
    ]

    operations = [
        migrations.AddField(
            model_name='woodmodel',
            name='factory',
            field=models.TextField(default='', max_length=64, verbose_name='厂家'),
        ),
    ]
