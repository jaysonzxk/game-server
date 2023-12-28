from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admin.game.models import GameCategory, Games, GameManufacturer
from apps.admin.op_drf.serializers import CustomModelSerializer


class GameCategorySerializer(CustomModelSerializer):
    """
    游戏大类序列化器
    """

    class Meta:
        model = GameCategory
        fields = '__all__'


class GameManufacturerSerializer(CustomModelSerializer):
    """
    游戏厂商序列化器
    """
    GameCategory = serializers.CharField()

    class Meta:
        model = GameManufacturer
        fields = '__all__'
