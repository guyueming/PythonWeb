# Generated by Django 3.2.3 on 2021-06-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='papermodel',
            name='color',
            field=models.TextField(default='', max_length=64, verbose_name='花色'),
        ),
    ]
