from django.db import models
from django.utils.timezone import now


class CustomerModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', max_length=64)
    address = models.TextField('地址', max_length=64)
    phone = models.TextField('电话', max_length=64)
    enable = models.BooleanField(
        '是否禁用', default=True, blank=False, null=False)
    note = models.TextField('备注', max_length=256, default='')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
