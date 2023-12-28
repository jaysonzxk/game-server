import django_filters
from django.contrib.auth import get_user_model

from apps.admin.game.models import GameCategory, GameManufacturer, Games



class GameCategoryFilter(django_filters.rest_framework.FilterSet):
    """
    游戏大类 简单序过滤器
    """

    class Meta:
        model = GameCategory
        fields = '__all__'


class GameManufacturerFilter(django_filters.rest_framework.FilterSet):
    """
    游戏厂商 简单序过滤器
    """

    class Meta:
        model = GameManufacturer
        fields = '__all__'


class GamesFilter(django_filters.rest_framework.FilterSet):
    """
    游戏 简单序过滤器
    """

    class Meta:
        model = Games
        fields = '__all__'
