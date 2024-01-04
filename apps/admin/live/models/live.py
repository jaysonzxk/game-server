from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE, DecimalField, \
    DateTimeField

from apps.admin.op_drf.models import CoreModel


class Tags(CoreModel):
    name = CharField(max_length=40, verbose_name="tag名称", null=True)
    sort = IntegerField(verbose_name='排序', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=1)

    class Meta:
        verbose_name = 'tag名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Lives(CoreModel):
    tag = ForeignKey(to='Tags', verbose_name='关联tag', on_delete=CASCADE, db_constraint=True,
                     null=True,
                     blank=True, related_name='tags')
    name = CharField(max_length=40, verbose_name="直播间名称", null=True)
    uri = CharField(max_length=140, verbose_name="封面", null=True)
    tickets = IntegerField(verbose_name='门票价格', null=True, blank=True, default=0)
    heatValue = IntegerField(verbose_name='热度值', null=True, blank=True, default=0)
    sort = IntegerField(verbose_name='排序', null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, default=1)

    class Meta:
        verbose_name = '直播间管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
