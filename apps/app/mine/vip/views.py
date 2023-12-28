from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.order.filters import QuantifyOrdersFilter, IncomeRankFilter
from apps.admin.order.models import QuantifyOrders
from apps.admin.order.models.order import IncomeRank
from apps.admin.order.serializers import QuantifyOrdersSerializer, IncomeRankSerializer
from apps.admin.pay.models import PayChannel
from apps.app.op_drf.response import SuccessResponse, ErrorResponse
from apps.app.op_drf.filters import DataLevelPermissionsFilter
from apps.app.op_drf.viewsets import CustomModelViewSet
from apps.admin.member.filters import VipCardFilter, UserVipCardFilter
from apps.admin.member.serializers import VipCardSerializer, UserVipCardSerializer
from apps.admin.member.models import VipCard, UserVip
from apps.app.utils.income_rank_data import generate_data
from apps.app.utils.json_response import DetailResponse
from apps.app.utils.pay import Pay


class ByVipModelViewSet(CustomModelViewSet):
    """
    购买vip 的CRUD视图
    """
    queryset = UserVip.objects.filter(isDel=0).filter(status=1)
    serializer_class = UserVipCardSerializer
    filter_class = UserVipCardFilter
    ordering = 'sort'  # 默认排序

    @transaction.atomic
    def buy_vip(self, request: Request, *args, **kwargs):
        jsonData = request.data
        vipObj = VipCard.objects.filter(id=jsonData.get('vipCard')).filter(isDel=0).filter(status=1).first()
        payChannelObj = PayChannel.objects.filter(id=jsonData.get('payChannelId')).filter(isDel=0).filter(status=1).first()
        user = request.user
        res = Pay().payVip(vipObj, payChannelObj, user, jsonData.get('payUri'))
        return SuccessResponse(msg=res)


class VipModelViewSet(CustomModelViewSet):
    """
    会员卡列表 的CRUD视图
    """
    queryset = VipCard.objects.filter(isDel=0).filter(status=1)
    serializer_class = VipCardSerializer
    authentication_classes = []
    permission_classes = []
    filter_class = VipCardFilter

    def get_vip_list(self, request: Request, *args, **kwargs):
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)
