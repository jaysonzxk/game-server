import django_filters
from django.contrib.auth import get_user_model

from apps.admin.order.models import QuantifyOrders, PurchaseVipOrders, PurchaseRobotOrders, PayOrders, IncomeRank

UserProfile = get_user_model()


class QuantifyOrdersFilter(django_filters.rest_framework.FilterSet):
    """
    量化订单 简单序过滤器
    """

    class Meta:
        model = QuantifyOrders
        fields = '__all__'


class PurchaseVipOrdersFilter(django_filters.rest_framework.FilterSet):
    """
    VIP购买订单 简单序过滤器
    """

    class Meta:
        model = PurchaseVipOrders
        fields = '__all__'


class PurchaseRobotOrdersFilter(django_filters.rest_framework.FilterSet):
    """
    机器人购买 简单序过滤器
    """

    class Meta:
        model = PurchaseRobotOrders
        fields = '__all__'


class PayOrdersFilter(django_filters.rest_framework.FilterSet):
    """
    抽点支付订单 简单序过滤器
    """

    class Meta:
        model = PayOrders
        fields = '__all__'


class IncomeRankFilter(django_filters.rest_framework.FilterSet):
    """
    收益排行 简单序过滤器
    """

    class Meta:
        model = IncomeRank
        fields = '__all__'
