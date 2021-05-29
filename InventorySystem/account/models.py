from django.db import models
from django.utils.timezone import now

FORM_TYPE = (
    ('1', '入库'),
    ('2', '出库'),
    ('3', '损耗'),
)


class AccountModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField('名称', max_length=64)
    is_enable = models.BooleanField(
        '是否禁用', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

