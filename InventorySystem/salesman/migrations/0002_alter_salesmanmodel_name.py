# Generated by Django 3.2.3 on 2021-06-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesmanmodel',
            name='name',
            field=models.TextField(max_length=64, unique=True, verbose_name='名称'),
        ),
    ]
