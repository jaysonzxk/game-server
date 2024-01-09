from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, DecimalField, \
    DateTimeField

from apps.admin.op_drf.models import CoreModel


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


class GameOrder(CoreModel):
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='order_game')
    game = ForeignKey(to='game.Games', verbose_name='关联游戏', null=True, blank=True, on_delete=CASCADE,
                      related_name='order_game')
    orderNo = CharField(verbose_name='订单编号', null=True, blank=True, max_length=500)
    betAmount = DecimalField(verbose_name='投注金额', null=True, blank=True, max_digits=15, decimal_places=2)
    incomeAmount = DecimalField(verbose_name='收益金额', null=True, blank=True, max_digits=15, decimal_places=2)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '投注订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"


class RewardOrder(CoreModel):
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='order_reward_user')
    live = ForeignKey(to='live.Lives', verbose_name='关联主播', null=True, blank=True, on_delete=CASCADE,
                      related_name='order_reward_live')
    orderNo = CharField(verbose_name='订单编号', null=True, blank=True, max_length=500)
    rewardAmount = IntegerField(verbose_name='打赏金额', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '打赏流水'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"


class WalletOrder(CoreModel):
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='wallet_reward_user')
    live = ForeignKey(to='live.Lives', verbose_name='关联主播', null=True, blank=True, on_delete=CASCADE,
                      related_name='wallet_reward_live')
    orderNo = CharField(verbose_name='订单编号', null=True, blank=True, max_length=500)
    rewardAmount = IntegerField(verbose_name='打赏金额', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '打赏流水'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"