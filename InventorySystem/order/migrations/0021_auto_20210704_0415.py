# Generated by Django 3.2.3 on 2021-07-04 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_auto_20210614_0135'),
        ('order', '0020_auto_20210704_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='specifications',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='process.specificationmodel', verbose_name='规格'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='technology',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='process.technologymodel', verbose_name='钢板工艺'),
        ),
    ]