from django.db import models
from django.db.models import Q
from django.utils.timezone import now


class PaperManager(models.Manager):
    def first_item(self, name):
        items = name.split('~')
        if len(items) == 3:
            q = Q(color=items[0])
            q.add(Q(type=items[1]), Q.AND)
            q.add(Q(factory=items[2]), Q.AND)
            return PaperModel.objects.filter(q).first()
        return None

    def query_str(self, name):
        q = Q()
        if name:
            q.add(Q(color__icontains=name), Q.OR)
            q.add(Q(type__icontains=name), Q.OR)
            q.add(Q(factory__icontains=name), Q.OR)
        return PaperModel.objects.filter(q)


class PaperModel(models.Model):
    id = models.AutoField(primary_key=True)
    color = models.TextField('花色', max_length=64, default="")
    type = models.TextField('型号', max_length=64, default="")
    factory = models.TextField('厂家', max_length=64, default="")
    count = models.IntegerField('数量', default=0)
    note = models.TextField('备注', max_length=256, default='')
    enable = models.BooleanField(
        '是否使用', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    objects = PaperManager()

    def __str__(self):
        return '%s~%s~%s' % (self.color, self.type, self.factory)
