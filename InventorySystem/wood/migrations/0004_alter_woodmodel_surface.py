# Generated by Django 3.2.3 on 2021-06-17 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wood', '0003_woodmodel_factory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woodmodel',
            name='surface',
            field=models.IntegerField(default=1, verbose_name='贴皮数'),
        ),
    ]
