from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, DecimalField

from apps.admin.op_drf.models import CoreModel


class Exchange(CoreModel):
    name = CharField(max_length=40, verbose_name="交易所名称", null=True)
    status = IntegerField(verbose_name="状态", null=True, default=1)

    class Meta:
        verbose_name = '交易所配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class UserExchangeConfig(CoreModel):
    exchange = ForeignKey(to='Exchange', verbose_name='关联交易所', null=True, blank=True, on_delete=CASCADE,
                          related_name='UserExchangeConfig_exchange')
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', null=True, blank=True, on_delete=CASCADE,
                      related_name='UserExchangeConfig_user')
    exchangeKey = CharField(max_length=200, verbose_name='交易所key', null=True)
    exchangeToken = CharField(max_length=200, verbose_name="token", null=True)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '用户交易所配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}"
