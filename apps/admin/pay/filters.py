import django_filters

from apps.admin.pay.models import PayChannel, AmountConfig


class PayChannelFilter(django_filters.rest_framework.FilterSet):
    """
    支付渠道 简单序过滤器
    """

    class Meta:
        model = PayChannel
        fields = '__all__'


class AmountConfigFilter(django_filters.rest_framework.FilterSet):
    """
    金额配置项 简单序过滤器
    """

    class Meta:
        model = AmountConfig
        fields = '__all__'
