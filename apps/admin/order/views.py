from django.contrib.auth import authenticate, get_user_model
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.op_drf.response import SuccessResponse, ErrorResponse
from apps.admin.op_drf.filters import DataLevelPermissionsFilter
from apps.admin.op_drf.viewsets import CustomModelViewSet
from apps.admin.order.filters import PurchaseVipOrdersFilter
from apps.admin.order.serializers import PurchaseVipOrdersSerializer
from apps.admin.order.models import PurchaseVipOrders


class PurchaseVipOrdersModelViewSet(CustomModelViewSet):
    """
    VIP购买订单 的CRUD视图
    """
    queryset = PurchaseVipOrders.objects.all()
    serializer_class = PurchaseVipOrdersSerializer
    filter_class = PurchaseVipOrdersFilter
    ordering = 'create_datetime'  # 默认排序



