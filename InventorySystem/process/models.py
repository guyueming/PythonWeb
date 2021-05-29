from django.db import models
from django.utils.timezone import now


class ProcessModel(models.Model):
    TYPE = (
        ('1', '工艺'),
        ('2', '规格'),
    )
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', max_length=64)
    type = models.CharField('类型', max_length=10, choices=TYPE, default='1')
    note = models.TextField('备注', max_length=256)
    is_enable = models.BooleanField(
        '是否禁用', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
