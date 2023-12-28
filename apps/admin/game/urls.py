from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.admin.game.views import GameCategoryModelViewSet, GameManufacturerViewSet, GamesModelViewSet

router = DefaultRouter()
router.register(r'gameCategory', GameCategoryModelViewSet)
router.register(r'gameManufacturer', GameManufacturerViewSet)
router.register(r'games', GamesModelViewSet)
urlpatterns = [
    # 游戏大类
    re_path('gameCategory/add', GameCategoryModelViewSet.as_view({'post': 'add_category'})),
    re_path('gameCategory/update', GameCategoryModelViewSet.as_view({'post': 'update_category'})),
    re_path('gameCategory/dalete', GameCategoryModelViewSet.as_view({'post': 'del_category'})),

    # 游戏厂商
    re_path('gameManufacturer/add', GameManufacturerViewSet.as_view({'post': 'add_manufacturer'})),
    re_path('gameManufacturer/update', GameManufacturerViewSet.as_view({'post': 'update_manufacturer'})),
    re_path('gameManufacturer/delete', GameManufacturerViewSet.as_view({'post': 'del_manufacturer'})),

    # 游戏
    re_path('games/add', GamesModelViewSet.as_view({'post': 'add_games'})),
    re_path('games/update', GamesModelViewSet.as_view({'post': 'update_games'})),
]
urlpatterns += router.urls
