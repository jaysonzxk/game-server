from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.admin.game.views import GameCategoryModelViewSet, GamesModelViewSet

router = DefaultRouter()
router.register(r'gameCategory', GameCategoryModelViewSet)
router.register(r'games', GamesModelViewSet)
urlpatterns = [
    # 游戏大类
    re_path('gameCategory/add', GameCategoryModelViewSet.as_view({'post': 'add_category'})),
    re_path('gameCategory/update', GameCategoryModelViewSet.as_view({'post': 'update_category'})),
    re_path('gameCategory/dalete', GameCategoryModelViewSet.as_view({'post': 'del_category'})),

    # 游戏
    re_path('games/add', GamesModelViewSet.as_view({'post': 'add_games'})),
    re_path('games/update', GamesModelViewSet.as_view({'post': 'update_games'})),
    re_path('category/list', GamesModelViewSet.as_view({'get': 'get_all_category'})),
]
urlpatterns += router.urls
