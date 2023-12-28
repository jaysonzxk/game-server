from django.contrib.auth import authenticate, get_user_model
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.op_drf.response import SuccessResponse, ErrorResponse
from apps.admin.op_drf.filters import DataLevelPermissionsFilter
from apps.admin.op_drf.viewsets import CustomModelViewSet
from apps.admin.order.filters import QuantifyOrdersFilter, PurchaseVipOrdersFilter, PurchaseRobotOrdersFilter, PayOrdersFilter
from apps.admin.order.serializers import QuantifyOrdersSerializer, PurchaseVipOrdersSerializer, PurchaseRobotOrdersSerializer, PayOrdersSerializer
from apps.admin.order.models import QuantifyOrders, PurchaseRobotOrders, PurchaseVipOrders, PayOrders


class QuantifyOrdersModelViewSet(CustomModelViewSet):
    """
    量化订单 的CRUD视图
    """
    queryset = QuantifyOrders.objects.all()
    serializer_class = QuantifyOrdersSerializer
    filter_class = QuantifyOrdersFilter
    ordering = 'create_datetime'  # 默认排序

    def list(self, request: Request, *args, **kwargs):
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            if getattr(self, 'values_queryset', None):
                return self.get_paginated_response(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if getattr(self, 'values_queryset', None):
            return SuccessResponse(page)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)


class PurchaseVipOrdersModelViewSet(CustomModelViewSet):
    """
    VIP购买订单 的CRUD视图
    """
    queryset = PurchaseVipOrders.objects.all()
    serializer_class = PurchaseVipOrdersSerializer
    filter_class = PurchaseVipOrdersFilter
    ordering = 'create_datetime'  # 默认排序


class PurchaseRobotOrdersModelViewSet(CustomModelViewSet):
    """
    机器人购买订单 的CRUD视图
    """
    queryset = PurchaseRobotOrders.objects.all()
    serializer_class = PurchaseRobotOrdersSerializer
    filter_class = PurchaseRobotOrdersFilter
    ordering = 'create_datetime'  # 默认排序


class PayOrdersModelViewSet(CustomModelViewSet):
    """
    交易所管理 的CRUD视图
    """
    queryset = PayOrders.objects.all()
    serializer_class = PayOrdersSerializer
    filter_class = PayOrdersFilter
    ordering = 'create_datetime'  # 默认排序

