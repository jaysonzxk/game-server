import django_filters
from django.contrib.auth import get_user_model

from apps.admin.order.models import PurchaseVipOrders, IncomeRank

UserProfile = get_user_model()


class PurchaseVipOrdersFilter(django_filters.rest_framework.FilterSet):
    """
    VIP购买订单 简单序过滤器
    """

    class Meta:
        model = PurchaseVipOrders
        fields = '__all__'


class IncomeRankFilter(django_filters.rest_framework.FilterSet):
    """
    收益排行 简单序过滤器
    """

    class Meta:
        model = IncomeRank
        fields = '__all__'
