from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, DecimalField, \
    DateTimeField

from apps.admin.op_drf.models import CoreModel


class Robot(CoreModel):
    name = CharField(max_length=40, verbose_name="机器人名称", null=True)
    robotType = IntegerField(verbose_name='机器人类型', default=0, null=True)
    originAmount = IntegerField(verbose_name="实际价格", null=True)
    vipAmount = IntegerField(verbose_name="会员价格", null=True)
    isRecommend = IntegerField(verbose_name='是否推荐', default=0, null=True, blank=True)
    # isDel = IntegerField(verbose_name='是否删除', null=True, default=0)
    status = IntegerField(verbose_name="状态", null=True, default=0)

    class Meta:
        verbose_name = '机器人管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class UserRobot(CoreModel):
    robot = ForeignKey(to='Robot', verbose_name='关联机器人', on_delete=CASCADE, db_constraint=True, null=True,
                       blank=True, related_name='UserRobot_robot')
    user = ForeignKey(to='permission.UserProfile', verbose_name='关联用户', on_delete=CASCADE, db_constraint=True,
                      null=True,
                      blank=True, related_name='UserRobot_user')
    expiration = DateTimeField(verbose_name='到期时间', null=True, blank=True, default=None)
    isExpiration = IntegerField(verbose_name='是否到期', default=0, null=True, blank=True)
    status = IntegerField(verbose_name='状态', default=0, null=True, blank=True)

    class Meta:
        verbose_name = '用户机器人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username}'
