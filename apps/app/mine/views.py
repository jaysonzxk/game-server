import time

from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.member.models import UserVip, UserRobot
from apps.admin.pay.filters import PayChannelFilter
from apps.admin.pay.models import payChannel, PayChannel
from apps.admin.pay.serializers import PayChannelSerializer
from apps.app.op_drf.response import SuccessResponse, ErrorResponse
from apps.app.op_drf.filters import DataLevelPermissionsFilter
from apps.app.op_drf.viewsets import CustomModelViewSet
from apps.admin.permission.filters import UserProfileFilter
from apps.admin.permission.serializers import UserProfileSerializer
from apps.admin.permission.models import UserProfile
from apps.admin.member.serializers import VipCardSerializer
from apps.admin.member.models import VipCard, Robot
from apps.admin.member.serializers import VipCardSerializer, RobotSerializer
from apps.admin.member.filters import VipCardFilter, RobotFilter


class UserModelViewSet(CustomModelViewSet):
    """
    用户 的CRUD视图
    """
    queryset = UserProfile.objects.filter(user_type=1)
    serializer_class = UserProfileSerializer
    filter_class = UserProfileFilter

    def user_info(self, request: Request, *args, **kwargs):
        user = request.user
        userVip = {}
        userRobot = {}
        try:
            userVipObj = UserVip.objects.filter(user_id=user.id).first()
            userRobotObj  = UserRobot.objects.filter(user_id=user.id).first()
            if userVipObj:
                userVip['name'] = userVipObj.vipCard.name
                userVip['expiration'] = userVipObj.expiration
                userVip['isExpiration'] = userVipObj.isExpiration
            if userRobotObj:
                userRobot['name'] = userRobotObj.robot.name
                userRobot['expiration'] = userRobotObj.expiration
                userRobot['isExpiration'] = userRobotObj.isExpiration
            if user:
                data = {
                    'id': user.id,
                    'avatar': user.avatar,
                    'username': user.username,
                    'name': user.name,
                    'phone': user.mobile,
                    'email': user.email,
                    'inviteCode': user.inviteCode,
                    'description': user.description,
                    'gender': user.gender,
                    'balance': user.balance,
                    'userVip': userVip if userVipObj else None,
                    'userRobot': userRobot if userRobotObj else None
                }
                return SuccessResponse(data=data)
        except Exception as e:
            return ErrorResponse(msg='未知错误')


class RobotModelViewSet(CustomModelViewSet):
    """
    机器人列表 的CRUD视图
    """
    queryset = Robot.objects.filter(isDel=0).filter(status=1)
    serializer_class = RobotSerializer
    authentication_classes = []
    permission_classes = []
    filter_class = RobotFilter

    def get_robot_list(self, request: Request, *args, **kwargs):
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)


class PayChannelModelViewSet(CustomModelViewSet):
    """
    支付渠道 的CRUD视图
    """
    queryset = PayChannel.objects.filter(isDel=0).filter(status=1)
    serializer_class = PayChannelSerializer
    authentication_classes = []
    permission_classes = []
    filter_class = PayChannelFilter

    def get_channel_list(self, request: Request, *args, **kwargs):
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)


class PromotionModelViewSet(CustomModelViewSet):
    """
    推广 的CRUD视图
    """
    queryset = UserProfile.objects.filter(isDel=0).filter(status=0)
    serializer_class = UserProfileSerializer
    filter_class = UserProfileFilter

    def get_promotion_list(self, request: Request, *args, **kwargs):
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        queryset = self.queryset.filter(parent_id=request.user.id)
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
