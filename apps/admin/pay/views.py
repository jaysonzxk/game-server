from django.contrib.auth import authenticate, get_user_model
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.op_drf.response import SuccessResponse, ErrorResponse
from apps.admin.op_drf.viewsets import CustomModelViewSet
from apps.admin.pay.filters import PayChannelFilter, AmountConfigFilter
from apps.admin.pay.serializers import PayChannelSerializer, AmountConfigSerializer
from apps.admin.pay.models import PayChannel, AmountConfig
from apps.admin.utils.qrCode import generate_qr_code


class PayChannelModelViewSet(CustomModelViewSet):
    """
    支付渠道 的CRUD视图
    """
    queryset = PayChannel.objects.all()
    serializer_class = PayChannelSerializer
    filter_class = PayChannelFilter
    ordering = 'sort'  # 默认排序

    @transaction.atomic
    def add_payChannel(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            try:
                qrCodePath = generate_qr_code(jsonData.ge('payCode'))
                jsonData['qrCode'] = qrCodePath
                payChannelObj = self.queryset.filter(name=jsonData.get('name'))
                if payChannelObj:
                    return ErrorResponse(msg='支付渠道已存在')
                serializer = PayChannelSerializer(data=jsonData)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return SuccessResponse(msg='新增成功')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_payChannel(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            try:
                qrCodePath = generate_qr_code(jsonData.ge('payCode'))
                payChannelObj = self.queryset.filter(id=jsonData.get('id')).first()
                if payChannelObj:
                    payChannelObj.name  = jsonData.get('name')
                    payChannelObj.minQuota  = jsonData.get('minQuota')
                    payChannelObj.maxQuota  = jsonData.get('maxQuota')
                    payChannelObj.payKey  = jsonData.get('payKey')
                    payChannelObj.payCode  = jsonData.get('payCode')
                    payChannelObj.sort  = jsonData.get('sort')
                    payChannelObj.status  = jsonData.get('status')
                    payChannelObj.qrCode  = qrCodePath
                    payChannelObj.save()
                    return SuccessResponse(msg='修改成功')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class AmountConfigModelViewSet(CustomModelViewSet):
    """
    金额配置 的CRUD视图
    """
    queryset = AmountConfig.objects.all()
    serializer_class = AmountConfigSerializer
    filter_class = AmountConfigFilter
    ordering = 'sort'  # 默认排序

    @transaction.atomic
    def add_amountConfig(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            try:
                serializer = AmountConfigSerializer(data=jsonData)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return SuccessResponse(msg='新增成功')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_amountConfig(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            try:
                amountConfigObj = self.queryset.filter(id=jsonData.get('id')).first()
                if amountConfigObj:
                    amountConfigObj.name  = jsonData.get('name')
                    amountConfigObj.originAmount  = jsonData.get('originAmount')
                    amountConfigObj.discountAmount  = jsonData.get('discountAmount')
                    amountConfigObj.sort  = jsonData.get('sort')
                    amountConfigObj.status  = jsonData.get('status')
                    amountConfigObj.description  = jsonData.get('description')
                    amountConfigObj.save()
                    return SuccessResponse(msg='修改成功')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')
