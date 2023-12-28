from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, DecimalField, \
    DateTimeField

from apps.admin.op_drf.models import CoreModel


class GameCategory(CoreModel):
    name = CharField(max_length=40, verbose_name="大类名称", null=True)
    image = CharField(max_length=140, verbose_name="封面图", null=True)
    sort = IntegerField(verbose_name='排序', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=1)

    class Meta:
        verbose_name = '大类名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class GameManufacturer(CoreModel):
    gameCategory = ForeignKey(to='GameCategory', verbose_name='关联类别', on_delete=CASCADE, db_constraint=True, null=True,
                              blank=True, related_name='gameCategory')
    name = CharField(max_length=40, verbose_name="厂商名称", null=True)
    image = CharField(max_length=140, verbose_name="封面图", null=True)
    sort = IntegerField(verbose_name='排序', null=True, blank=True)
    status = IntegerField(verbose_name='状态', default=1, null=True, blank=True)

    class Meta:
        verbose_name = '厂商名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}'


class Games(CoreModel):
    gameManufacturer = ForeignKey(to='GameManufacturer', verbose_name='关联厂商', on_delete=CASCADE, db_constraint=True,
                                  null=True,
                                  blank=True, related_name='gameManufacturer')
    name = CharField(max_length=40, verbose_name="游戏名称", null=True)
    image = CharField(max_length=140, verbose_name="封面图", null=True)
    url = CharField(max_length=500, verbose_name='跳转链接', null=True, blank=True)
    sort = IntegerField(verbose_name='排序', null=True, blank=True)
    isRecommend = IntegerField(verbose_name='推荐', default=0, null=True, blank=True)
    isHot = IntegerField(verbose_name='热门', default=0, null=True, blank=True)
    status = IntegerField(verbose_name='状态', default=1, null=True, blank=True)

    class Meta:
        verbose_name = '厂商名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}'
