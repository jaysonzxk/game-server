from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.admin.pay.views import PayChannelModelViewSet, AmountConfigModelViewSet

router = DefaultRouter()
router.register(r'payChannel', PayChannelModelViewSet)
router.register(r'amountConfig', AmountConfigModelViewSet)

urlpatterns = [
    re_path('payChannel/add', PayChannelModelViewSet.as_view({'post': 'add_payChannel'})),
    re_path('payChannel/update', PayChannelModelViewSet.as_view({'post': 'update_payChannel'})),
    re_path('amountConfig/add', AmountConfigModelViewSet.as_view({'post': 'add_amountConfig'})),
    re_path('amountConfig/update', AmountConfigModelViewSet.as_view({'post': 'update_amountConfig'})),
]
urlpatterns += router.urls
