from rest_framework import serializers

from apps.admin.op_drf.serializers import CustomModelSerializer
from apps.admin.pay.models import PayChannel, AmountConfig


class PayChannelSerializer(CustomModelSerializer):
    """
    支付渠道序列化器
    """

    class Meta:
        model = PayChannel
        fields = "__all__"


class AmountConfigSerializer(CustomModelSerializer):
    """
    金额配置项序列化器
    """

    class Meta:
        model = AmountConfig
        fields = "__all__"
