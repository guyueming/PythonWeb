from django.db import models
from django.utils.timezone import now
from account.models import AccountModel
from account.models import FORM_TYPE


class PaperModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', max_length=64)
    type = models.TextField('型号', max_length=64)
    factory = models.TextField('厂家', max_length=64)
    arrive_time = models.TextField('到货时间', default=now)
    count = models.IntegerField('数量', default=0)
    is_enable = models.BooleanField(
        '是否禁用', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)


class PaperFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    paper = models.ForeignKey(
        PaperModel,
        verbose_name='纸张',
        on_delete=models.PROTECT)
    count = models.IntegerField('数量', default=0)
    factory = models.TextField('厂家', max_length=64)
    arrive_time = models.TextField('到货时间', default=now)
    type = models.CharField('类型', max_length=10, choices=FORM_TYPE, default='1')
    is_sure = models.BooleanField(
        '是否确认', default=True, blank=False, null=False)
    user = models.ForeignKey(
        AccountModel,
        verbose_name='作者',
        on_delete=models.PROTECT)
    note = models.TextField('备注', max_length=256)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)