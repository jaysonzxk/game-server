from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.admin.live.views import TagsModelViewSet, LivesModelViewSet

router = DefaultRouter()
router.register(r'tag', TagsModelViewSet)
router.register(r'lives', LivesModelViewSet)
urlpatterns = [
    # tag
    re_path('tag/add', TagsModelViewSet.as_view({'post': 'add_tag'})),
    re_path('tag/update', TagsModelViewSet.as_view({'post': 'update_tag'})),
    re_path('tag/dalete', TagsModelViewSet.as_view({'post': 'del_tag'})),

    # 直播间
    re_path('lives/add', LivesModelViewSet.as_view({'post': 'add_live'})),
    re_path('lives/update', LivesModelViewSet.as_view({'post': 'update_live'})),
    re_path('lives/delete', LivesModelViewSet.as_view({'post': 'delete_live'})),
    re_path('tag/list', LivesModelViewSet.as_view({'get': 'get_all_tag'})),
]
urlpatterns += router.urls
