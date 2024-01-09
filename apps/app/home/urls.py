from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.app.home.views import BannersModelViewSet, AnnouncementModelViewSet, MarqueeModelViewSet, IncomeRankViewSet

router = DefaultRouter()
# router.register(r'banners', BannersModelViewSet)
# router.register(r'announcement', AnnouncementModelViewSet)
# router.register(r'marquee', MarqueeModelViewSet)
# router.register(r'incomeRank', IncomeRankViewSet)
urlpatterns = [
    re_path('incomeRank', IncomeRankViewSet.as_view({'get': 'get_income_rank_list'})),
    re_path('marquee', MarqueeModelViewSet.as_view({'get': 'get_marquee_list'})),
    re_path('banners', BannersModelViewSet.as_view({'get': 'get_banner_list'})),
    # re_path('income', IncomeViewSet.as_view({'get': 'get_income_list'})),
]
urlpatterns += router.urls
