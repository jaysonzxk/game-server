from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, DecimalField, \
    DateTimeField

from apps.admin.op_drf.models import CoreModel


class PayChannel(CoreModel):
    """ 支付渠道 """
    name = CharField(max_length=100, verbose_name='渠道名称', null=True, blank=True, help_text='渠道名称')
    minQuota = DecimalField(max_digits=15, decimal_places=6, verbose_name='最小限额', null=True, blank=True)
    maxQuota = DecimalField(max_digits=15, decimal_places=6, verbose_name='最大限额', null=True, blank=True)
    payKey = CharField(max_length=100, verbose_name='渠道key', null=True, blank=True, help_text='渠道key')
    payCode = CharField(max_length=100, verbose_name='支付编号', null=True, blank=True, help_text='支付编号')
    qrCode = CharField(max_length=200, verbose_name='二维码', null=True, blank=True, help_text='二维码')
    type = IntegerField(verbose_name='支付类型', null=True, blank=True, help_text='支付类型', default=0)
    sort = IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    status = IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=1)

    class Meta:
        verbose_name = '会员卡管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class AmountConfig(CoreModel):
    """ 充值金额配置 """
    name = CharField(max_length=100, verbose_name='配置项名称', null=True, blank=True, help_text='渠道名称')
    originAmount = IntegerField(verbose_name="实际价格", null=True)
    discountAmount = IntegerField(verbose_name="优惠价格", null=True)

    sort = IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    status = IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=1)

    class Meta:
        verbose_name = '充值金额配置管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
