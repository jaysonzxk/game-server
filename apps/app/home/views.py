from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.order.filters import QuantifyOrdersFilter, IncomeRankFilter
from apps.admin.order.models import QuantifyOrders
from apps.admin.order.models.order import IncomeRank
from apps.admin.order.serializers import QuantifyOrdersSerializer, IncomeRankSerializer
from apps.app.op_drf.response import SuccessResponse, ErrorResponse
from apps.app.op_drf.filters import DataLevelPermissionsFilter
from apps.app.op_drf.viewsets import CustomModelViewSet
from apps.admin.system.filters import BannersFilter, AnnouncementFilter, MarqueeFilter
from apps.admin.system.serializers import BannersSerializer, AnnouncementSerializer, MarqueeSerializer
from apps.admin.system.models import Banners, Announcement, Marquee
from apps.app.utils.income_rank_data import generate_data
from apps.app.utils.json_response import DetailResponse


class BannersModelViewSet(CustomModelViewSet):
    """
    轮播图 的CRUD视图
    """
    queryset = Banners.objects.filter(isDel=0).filter(status=1)
    serializer_class = BannersSerializer
    filter_class = BannersFilter
    authentication_classes = []
    permission_classes = []
    ordering = 'sort'  # 默认排序

    def get_banner_list(self, request: Request, *args, **kwargs):
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


class AnnouncementModelViewSet(CustomModelViewSet):
    """
    公告 的CRUD视图
    """
    queryset = Announcement.objects.filter(isDel=0).filter(status=1)
    serializer_class = AnnouncementSerializer
    filter_class = AnnouncementFilter
    authentication_classes = []
    permission_classes = []
    ordering = 'create_datetime'  # 默认排序


class MarqueeModelViewSet(CustomModelViewSet):
    """
    跑马灯  的CRUD视图
    """
    queryset = Marquee.objects.filter(isDel=0).filter(status=1)
    serializer_class = MarqueeSerializer
    filter_class = MarqueeFilter
    authentication_classes = []
    permission_classes = []
    ordering = 'create_datetime'  # 默认排序

    def get_marquee_list(self, request: Request, *args, **kwargs):
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


class IncomeRankViewSet(CustomModelViewSet):
    """
    收益排行  的CRUD视图
    """
    queryset = IncomeRank.objects.filter(status=1)
    serializer_class = IncomeRankSerializer
    filter_class = IncomeRankFilter
    authentication_classes = []
    permission_classes = []
    ordering = '-income'  # 默认排序

    def get_income_rank_list(self, request: Request, *args, **kwargs):
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


class IncomeViewSet(CustomModelViewSet):
    """
    收益展示  的CRUD视图
    """
    queryset = QuantifyOrders.objects.filter(status=1)
    serializer_class = QuantifyOrdersSerializer
    filter_class = QuantifyOrdersFilter
    authentication_classes = []
    permission_classes = []
    # ordering = '-income'  # 默认排序

    def get_income_list(self, request: Request, *args, **kwargs):
        res = generate_data(50)
        return DetailResponse(res)
