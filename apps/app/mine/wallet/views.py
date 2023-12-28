from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.app.op_drf.response import SuccessResponse, ErrorResponse
from apps.app.op_drf.viewsets import CustomModelViewSet
from apps.admin.pay.filters import AmountConfigFilter
from apps.admin.pay.serializers import AmountConfigSerializer
from apps.admin.pay.models import AmountConfig, PayChannel
from apps.app.utils.pay import Pay


class AmountConfigModelViewSet(CustomModelViewSet):
    """
    金额列表 的CRUD视图
    """
    queryset = AmountConfig.objects.filter(isDel=0).filter(status=1)
    serializer_class = AmountConfigSerializer
    authentication_classes = []
    permission_classes = []
    filter_class = AmountConfigFilter
    ordering = 'sort'  # 默认排序

    def get_amount_list(self, request: Request, *args, **kwargs):
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)


class RechargeModelViewSet(CustomModelViewSet):
    """
    充值余额 的CRUD视图
    """
    queryset = AmountConfig.objects.filter(isDel=0).filter(status=1)
    serializer_class = AmountConfigSerializer
    filter_class = AmountConfigFilter

    @transaction.atomic
    def recharge_balance(self, request: Request, *args, **kwargs):
        jsonData = request.data
        rechargeObj = self.queryset.filter(id=jsonData.get('amount')).filter(isDel=0).filter(status=1).first()
        payChannelObj = PayChannel.objects.filter(id=jsonData.get('payChannelId')).filter(isDel=0).filter(status=1).first()
        user = request.user
        res = Pay().rechargeBalance(rechargeObj, payChannelObj, user, jsonData.get('payUri'))
        return SuccessResponse(msg=res)

