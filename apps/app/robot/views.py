from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.member.models import UserVip, UserRobot, UserExchangeConfig
from apps.admin.order.models import PayOrders
from apps.app.op_drf.response import SuccessResponse, ErrorResponse
from apps.app.op_drf.filters import DataLevelPermissionsFilter
from apps.app.op_drf.viewsets import CustomModelViewSet
from apps.admin.member.filters import UserRobotFilter
from apps.admin.member.serializers import UserRobotSerializer
from apps.admin.member.models import UserRobot


class UserRobotModelViewSet(CustomModelViewSet):
    """
    机器人 的CRUD视图
    """
    queryset = UserRobot.objects.all()
    serializer_class = UserRobotSerializer
    filter_class = UserRobotFilter

    @transaction.atomic
    def change_robot(self, request: Request, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            userRobotObj = self.queryset.filter(user_id=user.id).first()
            payOrdersObj = PayOrders.objects.filter(user_id=user.id).filter(status=0)
            userExchangeConfigObj = UserExchangeConfig.objects.filter(user_id=user.id).filter(isDel=0)
            if data:
                if userExchangeConfigObj.count() == 0 and data.get('status') == 1:
                    return ErrorResponse(msg='未配置交易所,开启失败')
                if payOrdersObj.count() > 0 and data.get('status') == 1:
                    return ErrorResponse(msg='有未结算账单,开启失败')
                if userRobotObj:
                    if userRobotObj.isExpiration == 1:
                        return ErrorResponse(msg='机器人已到期~')
                    userRobotObj.status = data.get('status')
                    userRobotObj.save()
                    msg = '开启成功' if data.get('status') == 1 else '关闭成功'
                    return SuccessResponse(msg=msg)
                else:
                    return ErrorResponse(msg='您还没开通机器人~')
            return ErrorResponse(msg='参数错误')
        except Exception as e:
            return ErrorResponse(msg='未知错误')
