from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from salesman.models import SalesmanModel
from customer.models import CustomerModel
from paper.models import PaperModel
from wood.models import WoodModel
from skin.models import SkinModel
from process.models import TechnologyModel, SpecificationModel


FORM_TYPE = (
    ('1', '入库'),
    ('2', '出库'),
    ('3', '损耗'),
    ('4', '订单'),
)


class OrderNumberModel(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.IntegerField('下单时间', default=0)
    order_number = models.IntegerField('订单编号', default=0)

    objects = models.manager


class OrderHeadModel(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.IntegerField('订单编号', default=0)
    order_date = models.DateField('下单时间', default=now)
    delivery_date = models.DateField('交货时间', default=now)
    salesman = models.ForeignKey(
        SalesmanModel,
        verbose_name='销售员',
        on_delete=models.PROTECT, null=True)
    customer = models.ForeignKey(
        CustomerModel,
        verbose_name='厂家',
        on_delete=models.PROTECT, null=True)
    sure = models.BooleanField(
        '是否确认', default=False, blank=False, null=False)
    complete = models.BooleanField(
        '是否完成', default=False, blank=False, null=False)
    note = models.TextField('备注', max_length=256, default='')
    user = models.ForeignKey(
        User,
        verbose_name='作者',
        on_delete=models.PROTECT, null=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    objects = models.manager

    def __str__(self):
        return self.order_number


class OrderModel(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    head_number = models.ForeignKey(
        OrderHeadModel,
        verbose_name='订单编号',
        on_delete=models.PROTECT, null=True)
    wood = models.ForeignKey(
        WoodModel,
        verbose_name='木料',
        on_delete=models.PROTECT)
    woodCount = models.IntegerField('木料数量', default=0)
    skin = models.ForeignKey(
        SkinModel,
        verbose_name='桉木皮',
        on_delete=models.PROTECT, null=True, blank=True)
    skinCount = models.IntegerField('桉木皮数量', default=0, blank=True)
    paper = models.ForeignKey(
        PaperModel,
        verbose_name='纸张1',
        on_delete=models.PROTECT, null=True, blank=True)
    paperCount = models.IntegerField('纸张数量', default=0, blank=True)
    other_paper = models.ForeignKey(
        PaperModel,
        verbose_name='纸张2',
        related_name='other_paper',
        on_delete=models.PROTECT, null=True, blank=True)
    other_paper_count = models.IntegerField('纸张数量', default=0, blank=True)
    technology = models.ForeignKey(
        TechnologyModel,
        verbose_name='钢板工艺',
        on_delete=models.PROTECT, null=True, blank=True)
    specifications = models.ForeignKey(
        SpecificationModel,
        verbose_name='规格',
        on_delete=models.PROTECT, null=True, blank=True)
    packaging = models.TextField('包装', max_length=64, default='', blank=True)
    thickness = models.TextField('厚度', max_length=64, default='', blank=True)
    trademark = models.TextField('商标', max_length=64, default='', blank=True)
    word = models.TextField('打字', max_length=64, default='', blank=True)
    is_grooving = models.BooleanField(
        '是否开槽', default=False, blank=False)
    is_drying = models.BooleanField(
        '是否烘干', default=False, blank=False)
    sure = models.BooleanField(
        '是否确认', default=False, blank=False)
    note = models.TextField('备注', max_length=256, default='', blank=True)
    user = models.ForeignKey(
        User,
        verbose_name='作者',
        on_delete=models.PROTECT, null=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    objects = models.Manager()


class WoodFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(
        WoodModel,
        verbose_name='木料',
        on_delete=models.PROTECT)
    arrive_date = models.DateField('到货时间', default=now)
    count = models.IntegerField('数量', default=0)
    type = models.CharField('类型', max_length=4, choices=FORM_TYPE, default='1')
    order = models.ForeignKey(
        OrderModel,
        verbose_name='关联订单',
        on_delete=models.CASCADE, null=True)
    sure = models.BooleanField(
        '是否确认', default=False, blank=False, null=False)
    complete = models.BooleanField(
        '是否完成', default=False, blank=False, null=False)
    user = models.ForeignKey(
        User,
        verbose_name='作者',
        on_delete=models.PROTECT, null=True)
    note = models.TextField('备注', max_length=256, default='')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    objects = models.Manager()


class SkinFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    arrive_date = models.DateField('到货时间', default=now)
    name = models.ForeignKey(
        SkinModel,
        verbose_name='桉木皮',
        on_delete=models.PROTECT)
    count = models.IntegerField('数量', default=0)
    type = models.CharField('类型', max_length=4, choices=FORM_TYPE, default='1')
    sure = models.BooleanField(
        '是否确认', default=False, blank=False, null=False)
    complete = models.BooleanField(
        '是否完成', default=False, blank=False, null=False)
    order = models.ForeignKey(
        OrderModel,
        verbose_name='关联订单',
        on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User,
        verbose_name='作者',
        on_delete=models.PROTECT, null=True)
    note = models.TextField('备注', max_length=256, default='')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    objects = models.Manager()


class PaperFormModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(
        PaperModel,
        verbose_name='纸张',
        on_delete=models.PROTECT)
    count = models.IntegerField('数量', default=0)
    factory = models.TextField('厂家', max_length=64)
    arrive_date = models.DateField('到货时间', default=now)
    type = models.CharField('类型', max_length=4, choices=FORM_TYPE, default='1')
    sure = models.BooleanField(
        '是否确认', default=False, blank=False, null=False)
    complete = models.BooleanField(
        '是否确认', default=False, blank=False, null=False)
    order = models.ForeignKey(
        OrderModel,
        verbose_name='关联订单',
        on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        User,
        verbose_name='作者',
        on_delete=models.PROTECT, null=True)
    note = models.TextField('备注', max_length=256, default='')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    objects = models.Manager()
