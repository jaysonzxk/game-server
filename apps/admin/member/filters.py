import django_filters
from django.contrib.auth import get_user_model

from apps.admin.member.models import VipCard, UserVip
from apps.admin.utils.model_util import get_dept

UserProfile = get_user_model()


class MemberFilter(django_filters.rest_framework.FilterSet):
    """
    用户管理 简单序过滤器
    """
    username = django_filters.CharFilter(lookup_expr='icontains')
    mobile = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = UserProfile
        exclude = ('secret', 'password',)


class VipCardFilter(django_filters.rest_framework.FilterSet):
    """
    会员卡 简单序过滤器
    """

    class Meta:
        model = VipCard
        fields = '__all__'


class UserVipCardFilter(django_filters.rest_framework.FilterSet):
    """
    会员卡 简单序过滤器
    """

    class Meta:
        model = UserVip
        fields = '__all__'
