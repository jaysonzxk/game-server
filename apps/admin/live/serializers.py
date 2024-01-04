from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admin.live.models import Tags, Lives
from apps.admin.op_drf.serializers import CustomModelSerializer


class TagsSerializer(CustomModelSerializer):
    """
    Tags序列化器
    """

    class Meta:
        model = Tags
        fields = '__all__'


# class GameManufacturerSerializer(CustomModelSerializer):
#     """
#     游戏厂商序列化器
#     """
#     gameCategory = serializers.IntegerField(source='gameCategory_id')
#
#     class Meta:
#         model = GameManufacturer
#         fields = '__all__'


class LivesSerializer(CustomModelSerializer):
    """
    直播间序列化器
    """
    tag = serializers.IntegerField(source='tag_id')

    class Meta:
        model = Lives
        fields = '__all__'
