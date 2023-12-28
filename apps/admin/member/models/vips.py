from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, DecimalField, DateTimeField

from apps.admin.op_drf.models import CoreModel


class VipCard(CoreModel):
    name = CharField(max_length=40, verbose_name="会员卡名称", null=True)
    originAmount = IntegerField(verbose_name="实际价格", null=True)
    discountAmount = IntegerField(verbose_name="优惠价格", null=True)
    vipCardType = IntegerField(verbose_name='会员卡类型', null=True, blank=True)
    recommend = IntegerField(verbose_name='是否推荐', default=0, null=True, blank=True)
    # isDel = IntegerField(verbose_name='是否删除', null=True, default=0)
    status = IntegerField(verbose_name="状态", null=True, default=1)

    class Meta:
        verbose_name = '会员卡管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class UserVip(CoreModel):
    vipCard = ForeignKey(to='VipCard', verbose_name='管理会员卡', on_delete=CASCADE, db_constraint=True, null=True,
                         blank=True, related_name='UserVip_card')
    user = ForeignKey(to='permission.UserProfile', verbose_name='管理用户', on_delete=CASCADE, db_constraint=True, null=True,
                         blank=True, related_name='UserVip_user')
    expiration = DateTimeField(verbose_name='到期时间', null=True, blank=True, default=None)
    isExpiration = IntegerField(verbose_name='是否到期', default=0, null=True, blank=True)
    isRecommend = IntegerField(verbose_name='是否推荐', default=0, null=True, blank=True)
    # isDel = IntegerField(verbose_name='是否删除', null=True, default=0)
    status = IntegerField(verbose_name='状态', default=1, null=True, blank=True)

    class Meta:
        verbose_name = '用户会员卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username}'
