from django.db import models
from django.utils.timezone import now
from account.models import AccountModel, FORM_TYPE
from salesman.models import SalesmanModel
from customer.models import CustomerModel
from paper.models import PaperModel
from wood.models import WoodModel
from skin.models import SkinModel
from process.models import TechnologyModel, SpecificationModel


class OrderModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField('日期', max_length=64)
    salesman = models.ForeignKey(
        SalesmanModel,
        verbose_name='销售员',
        on_delete=models.PROTECT)
    factory = models.ForeignKey(
        CustomerModel,
        # to_fields=CustomerModel.name,
        verbose_name='厂家',
        on_delete=models.PROTECT)
    wood = models.ForeignKey(
        WoodModel,
        # to_fields=WoodModel.name,
        verbose_name='材质',
        on_delete=models.PROTECT)
    woodCount = models.TextField('木料数量', max_length=64)
    skin = models.ForeignKey(
        SkinModel,
        # to_fields=SkinModel.name,
        verbose_name='桉木皮',
        on_delete=models.PROTECT)
    skinCount = models.TextField('桉木皮数量', max_length=64)
    paper = models.ForeignKey(
        PaperModel,
        # to_fields=PaperModel.name,
        verbose_name='纸张',
        on_delete=models.PROTECT)
    paperCount = models.TextField('纸张数量', max_length=64)
    color = models.TextField('花色', max_length=64)
    technology = models.ForeignKey(
        TechnologyModel,
        # to_fields=TechnologyModel.name,
        verbose_name='钢铁工艺',
        on_delete=models.PROTECT)
    specifications = models.ForeignKey(
        SpecificationModel,
        # to_fields=SpecificationModel.name,
        verbose_name='规格',
        on_delete=models.PROTECT)
    packaging = models.TextField('包装', max_length=64)
    thickness = models.TextField('厚度', max_length=64)
    trademark = models.TextField('商标', max_length=64)
    word = models.TextField('打字', max_length=64)
    is_grooving = models.BooleanField(
        '是否开槽', default=True, blank=False, null=False)
    is_drying = models.BooleanField(
        '是否烘干', default=True, blank=False, null=False)
    sure = models.BooleanField(
        '是否确认', default=True, blank=False, null=False)
    sure_time = models.DateTimeField('确认时间', default=now)
    complete = models.BooleanField(
        '是否完成', default=True, blank=False, null=False)
    complete_time = models.DateTimeField('完成时间', default=now)
    note = models.TextField('备注', max_length=256, default='')
    user = models.ForeignKey(
        AccountModel,
        # to_fields=AccountModel.name,
        verbose_name='作者',
        on_delete=models.PROTECT)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)


class WoodFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(
        WoodModel,
        verbose_name='木料',
        on_delete=models.PROTECT)
    arrive_time = models.DateTimeField('到货时间', default=now)
    count = models.IntegerField('数量', default=0)
    type = models.CharField('类型', max_length=4, choices=FORM_TYPE, default='1')
    order = models.ForeignKey(
        OrderModel,
        verbose_name='关联订单',
        on_delete=models.CASCADE, null=True)
    sure = models.BooleanField(
        '是否确认', default=True, blank=False, null=False)
    user = models.ForeignKey(
        AccountModel,
        verbose_name='作者',
        on_delete=models.PROTECT, null=True)
    note = models.TextField('备注', max_length=256, default='')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)


class SkinFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    arrive_time = models.DateTimeField('到货时间', default=now)
    name = models.ForeignKey(
        SkinModel,
        verbose_name='桉木皮',
        on_delete=models.PROTECT)
    count = models.IntegerField('数量', default=0)
    type = models.CharField('类型', max_length=4, choices=FORM_TYPE, default='1')
    sure = models.BooleanField(
        '是否确认', default=True, blank=False, null=False)
    order = models.ForeignKey(
        OrderModel,
        verbose_name='关联订单',
        on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        AccountModel,
        verbose_name='作者',
        on_delete=models.PROTECT, null=True)
    note = models.TextField('备注', max_length=256, default='')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)


class PaperFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(
        PaperModel,
        verbose_name='纸张',
        on_delete=models.PROTECT)
    count = models.IntegerField('数量', default=0)
    factory = models.TextField('厂家', max_length=64)
    arrive_time = models.TextField('到货时间', default=now)
    type = models.CharField('类型', max_length=4, choices=FORM_TYPE, default='1')
    sure = models.BooleanField(
        '是否确认', default=True, blank=False, null=False)
    order = models.ForeignKey(
        OrderModel,
        verbose_name='关联订单',
        on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        AccountModel,
        verbose_name='作者',
        on_delete=models.PROTECT, null=True)
    note = models.TextField('备注', max_length=256, default='')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
