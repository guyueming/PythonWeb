# Generated by Django 3.2.3 on 2021-07-11 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0003_auto_20210618_0709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='papermodel',
            name='name',
        ),
    ]
