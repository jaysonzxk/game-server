from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.admin.order.views import PurchaseVipOrdersModelViewSet

router = DefaultRouter()
router.register(r'purchaseVipOrders', PurchaseVipOrdersModelViewSet)

urlpatterns = [
    # re_path('monitor/info/(?P<pk>.*)/', MonitorModelViewSet.as_view({'get': 'get_monitor_info'})),
    # re_path('monitor/rate/(?P<pk>.*)/', MonitorModelViewSet.as_view({'get': 'get_rate_info'})),
    # re_path('monitor/enabled/', MonitorModelViewSet.as_view({'get': 'enabled_monitor_info'})),
    # re_path('monitor/clean/', MonitorModelViewSet.as_view({'get': 'clean_all'})),
]
urlpatterns += router.urls
