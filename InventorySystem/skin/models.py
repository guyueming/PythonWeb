from django.db import models
from django.utils.timezone import now
from django.conf import settings
from account.models import AccountModel


class SkinModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', max_length=64)
    count = models.IntegerField('数量', default=0)
    is_enable = models.BooleanField(
        '是否禁用', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)


class SkinFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    skin = models.ForeignKey(
        SkinModel,
        verbose_name='桉木皮',
        on_delete=models.PROTECT)
    count = models.IntegerField('数量', default=0)
    is_sure = models.BooleanField(
        '是否确认', default=True, blank=False, null=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='作者',
        on_delete=models.PROTECT)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
