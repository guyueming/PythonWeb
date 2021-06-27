from django.db import models
from django.utils.timezone import now


class SalesmanModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', max_length=64, unique=True, null=False)
    phone = models.TextField('电话', max_length=64)
    note = models.TextField('备注', max_length=256, default='')
    enable = models.BooleanField(
        '是否使用', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    objects = models.manager

    def update_enable_state(self, mid):
        obj = self.objects.get(id=mid)
        obj.enable = obj.enable
        obj.save()

    def __str__(self):
        return self.name
