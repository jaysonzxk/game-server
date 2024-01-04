from rest_framework import serializers

from apps.admin.op_drf.serializers import CustomModelSerializer
from apps.admin.order.models import PurchaseVipOrders, IncomeRank


class PurchaseVipOrdersSerializer(CustomModelSerializer):
    """
    购买VIP 序列化器
    """
    user = serializers.CharField(read_only=True)
    vipCard = serializers.CharField(read_only=True)

    # def create(self, validated_data):
    #     buyVipOrders = PurchaseVipOrders.objects.create(**validated_data)
    #     return buyVipOrders

    class Meta:
        model = PurchaseVipOrders
        fields = "__all__"


class IncomeRankSerializer(CustomModelSerializer):
    """
    收益排行 序列化器
    """
    user = serializers.CharField(source='user.name')

    class Meta:
        model = IncomeRank
        fields = ('user', 'income',)
