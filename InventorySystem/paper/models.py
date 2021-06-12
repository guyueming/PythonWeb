from django.db import models
from django.utils.timezone import now
from account.models import AccountModel
from account.models import FORM_TYPE


class PaperModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', max_length=64)
    type = models.TextField('型号', max_length=64)
    factory = models.TextField('厂家', max_length=64)
    count = models.IntegerField('数量', default=0)
    note = models.TextField('备注', max_length=256, default='')
    enable = models.BooleanField(
        '是否禁用', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
