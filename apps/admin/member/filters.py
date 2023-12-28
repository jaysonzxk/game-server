import django_filters
from django.contrib.auth import get_user_model

from apps.admin.member.models import VipCard, UserVip, UserExchangeConfig, Robot, UserRobot
from apps.admin.member.models.userExchangeConfig import Exchange
from apps.admin.utils.model_util import get_dept

UserProfile = get_user_model()


class UserProfileFilter(django_filters.rest_framework.FilterSet):
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


class ExchangeFilter(django_filters.rest_framework.FilterSet):
    """
    交易所 简单序过滤器
    """

    class Meta:
        model = Exchange
        fields = '__all__'


class UserExchangeConfigFilter(django_filters.rest_framework.FilterSet):
    """
    用户交易所 简单序过滤器
    """

    class Meta:
        model = UserExchangeConfig
        fields = '__all__'


class RobotFilter(django_filters.rest_framework.FilterSet):
    """
    机器人 简单序过滤器
    """

    class Meta:
        model = Robot
        fields = '__all__'


class UserRobotFilter(django_filters.rest_framework.FilterSet):
    """
    用户机器人 简单序过滤器
    """

    class Meta:
        model = UserRobot
        fields = '__all__'
