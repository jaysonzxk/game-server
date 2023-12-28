from django.db.models import CharField, ForeignKey, BooleanField, CASCADE, IntegerField, DateTimeField

from apps.admin.op_drf.models import CoreModel


class Banners(CoreModel):
    name = CharField(max_length=64, verbose_name="banner名称", null=True, blank=True)
    jumpType = IntegerField(verbose_name="跳转类型", null=True, blank=True)
    jumpUrl = CharField(max_length=256, verbose_name="跳转地址", null=True, blank=True)
    uri = CharField(max_length=100, verbose_name='图片路径', null=True, blank=True)
    sort = IntegerField(verbose_name="排序", null=True, blank=True, default=0)
    expiration = DateTimeField(verbose_name='到期时间', null=True, blank=True, default=None)
    isExpiration = IntegerField(verbose_name='是否到期', default=0, null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, blank=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Announcement(CoreModel):
    name = CharField(max_length=64, verbose_name="公告名称", null=True, blank=True)
    content = CharField(max_length=500, verbose_name="公告内容", null=True, blank=True)
    sort = IntegerField(verbose_name="排序", null=True, blank=True, default=0)
    expiration = DateTimeField(verbose_name='到期时间', null=True, blank=True, default=None)
    isExpiration = IntegerField(verbose_name='是否到期', default=0, null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, blank=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Marquee(CoreModel):
    name = CharField(max_length=64, verbose_name="跑马灯名称", null=True, blank=True)
    content = CharField(max_length=500, verbose_name="跑马灯内容", null=True, blank=True)
    expiration = DateTimeField(verbose_name='到期时间', null=True, blank=True, default=None)
    isExpiration = IntegerField(verbose_name='是否到期', default=0, null=True, blank=True)
    status = IntegerField(verbose_name="状态", null=True, blank=True)

    class Meta:
        verbose_name = '跑马灯'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
