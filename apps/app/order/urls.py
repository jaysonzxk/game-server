from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.app.home.views import BannersModelViewSet, AnnouncementModelViewSet, MarqueeModelViewSet

router = DefaultRouter()
router.register(r'banners', BannersModelViewSet)
router.register(r'announcement', AnnouncementModelViewSet)
router.register(r'marquee', MarqueeModelViewSet)
urlpatterns = [
]
urlpatterns += router.urls
