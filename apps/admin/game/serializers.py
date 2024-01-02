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
    gameCategory = serializers.IntegerField(source='gameCategory_id')

    class Meta:
        model = GameManufacturer
        fields = '__all__'


class GamesSerializer(CustomModelSerializer):
    """
    游戏序列化器
    """
    gameManufacturer = serializers.IntegerField(source='gameManufacturer_id')

    # _name = serializers.CharField(read_only=True, source='gameManufacturer_name')

    class Meta:
        model = Games
        fields = '__all__'
