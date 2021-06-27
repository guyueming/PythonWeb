from django.db import models
from django.utils.timezone import now


class PaperModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', max_length=64, unique=False, null=False)
    color = models.TextField('花色', max_length=64, default="")
    type = models.TextField('型号', max_length=64, default="")
    factory = models.TextField('厂家', max_length=64, default="")
    count = models.IntegerField('数量', default=0)
    note = models.TextField('备注', max_length=256, default='')
    enable = models.BooleanField(
        '是否使用', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    objects = models.manager

    def __str__(self):
        return '%s-%s-%s-%s' % (self.name, self.color, self.type,  self.factory)
