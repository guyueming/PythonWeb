# Generated by Django 3.2.3 on 2021-07-08 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_auto_20210707_0222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='index',
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
