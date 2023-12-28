from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, DecimalField, \
    DateTimeField

from apps.admin.op_drf.models import CoreModel


class QuantifyOrders(CoreModel):
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='QuantifyOrders_user')
    robot = ForeignKey(to='member.UserRobot', verbose_name='关联用户机器人', null=True, blank=True, on_delete=CASCADE,
                       related_name='QuantifyOrders_robot')
    orderNumber = CharField(max_length=100, verbose_name='订单单号', null=True, blank=True)
    investmentAmount = DecimalField(max_digits=15, decimal_places=6, verbose_name='投资金额', null=True, blank=True)
    income = DecimalField(max_digits=15, decimal_places=6, verbose_name='收益', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '量化订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"


class PurchaseVipOrders(CoreModel):
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='PurchaseVipOrders_user')
    vipCard = ForeignKey(to='member.VipCard', verbose_name='关联vip卡', null=True, blank=True, on_delete=CASCADE,
                         related_name='PurchaseVipOrders_robot')
    payChannel = ForeignKey(to='pay.PayChannel', verbose_name='关联支付', null=True, blank=True, on_delete=CASCADE,
                            related_name='PurchaseVipOrders_payChannel')
    realAmount = IntegerField(verbose_name="会员价格", null=True)
    payUri = CharField(max_length=100, verbose_name='支付截图', null=True, blank=True)
    orderNumber = CharField(max_length=100, verbose_name='订单单号', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '购买VIP订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"


class PurchaseRobotOrders(CoreModel):
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='PurchaseRobotOrders_user')
    robot = ForeignKey(to='member.Robot', verbose_name='关联机器人', null=True, blank=True, on_delete=CASCADE,
                       related_name='PurchaseRobotOrders_robot')
    realAmount = IntegerField(verbose_name="会员价格", null=True)
    orderNumber = CharField(max_length=100, verbose_name='订单单号', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '购买机器人订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"


class PayOrders(CoreModel):
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='PayOrders_user')
    quantifyOrders = ForeignKey(to='QuantifyOrders', verbose_name='关联交易订单', null=True, blank=True,
                                on_delete=CASCADE,
                                related_name='PayOrders_order')
    orderNumber = CharField(max_length=100, verbose_name='订单单号', null=True, blank=True)
    payAmount = DecimalField(max_digits=15, decimal_places=6, verbose_name='抽点金额', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '抽点支付订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"


class IncomeRank(CoreModel):
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='PayOrders_order')
    income = DecimalField(max_digits=15, decimal_places=6, verbose_name='抽点金额', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '收益排行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"
