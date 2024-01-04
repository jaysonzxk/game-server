from django.contrib.auth import authenticate, get_user_model
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.member.models.userExchangeConfig import Exchange
from apps.admin.op_drf.response import SuccessResponse, ErrorResponse
from apps.admin.op_drf.filters import DataLevelPermissionsFilter
from apps.admin.op_drf.viewsets import CustomModelViewSet
from apps.admin.member.filters import MemberFilter, VipCardFilter, UserVipCardFilter, ExchangeFilter, \
    UserExchangeConfigFilter, RobotFilter, UserRobotFilter
from apps.admin.member.serializers import MemberSerializer, UserVipCardSerializer, VipCardSerializer, \
    ExchangeSerializer, UserExchangeConfigSerializer, RobotSerializer, UserRobotSerializer
from apps.admin.member.models import VipCard, UserVip, UserExchangeConfig, Robot, UserRobot

UserProfile = get_user_model()


class GetUserProfileView(APIView):
    """
    获取用户详细信息
    """

    def get(self, request, format=None):
        user_dict = MemberSerializer(request.user).data

        return SuccessResponse({
            'user': user_dict
        })


class UserProfileModelViewSet(CustomModelViewSet):
    """
    用户管理 的CRUD视图
    """
    queryset = UserProfile.objects.filter(user_type=1)
    serializer_class = MemberSerializer
    filter_class = MemberFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    search_fields = ('username',)
    ordering = 'create_datetime'  # 默认排序

    def change_status(self, request: Request, *args, **kwargs):
        """
        修改用户状态
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.data.get('userId'))
        instance.is_active = request.data.get('status')
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def get_user_details(self, request: Request, *args, **kwargs):
        """
        获取用户详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        userId = request.query_params.get('userId')
        data = {
        }
        if userId:
            instance = self.queryset.get(id=userId)
            serializer = self.get_serializer(instance)
            data['data'] = serializer.data
            data['postIds'] = [ele.get('id') for ele in serializer.data.get('post')]
            data['roleIds'] = [ele.get('id') for ele in serializer.data.get('role')]
            if hasattr(self, 'handle_logging'):
                self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(data)

    def profile(self, request: Request, *args, **kwargs):
        """
        获取用户个人信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.user.id)
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def put_profile(self, request: Request, *args, **kwargs):
        """
        更新用户个人信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.user.id)
        instance.name = request.data.get('name', None)
        instance.mobile = request.data.get('mobile', None)
        instance.email = request.data.get('email', None)
        instance.gender = request.data.get('gender', None)
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def put_avatar(self, request: Request, *args, **kwargs):
        """
        更新用户头像
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.queryset.get(id=request.user.id)
        instance.avatar = request.data.get('avatar_url', None)
        instance.save()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)


class VipCardModelViewSet(CustomModelViewSet):
    """
    会员卡管理 的CRUD视图
    """
    queryset = VipCard.objects.filter(isDel=0)
    serializer_class = VipCardSerializer
    filter_class = VipCardFilter
    ordering = 'create_datetime'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_vip_card(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            vipObj = self.queryset.filter(name=jsonData.get('name')).first()
            if vipObj:
                return ErrorResponse(msg='该会员卡已存在')
            serializer = VipCardSerializer(data=jsonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return SuccessResponse(msg='新增成功')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_vip_card(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(id=jsonData.get('id')).first()
                if instance:
                    instance.name = jsonData.get('name')
                    instance.originAmount = jsonData.get('originAmount')
                    instance.discountAmount = jsonData.get('discountAmount')
                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                return ErrorResponse(msg='会员卡不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    def del_vip_card(self, request: Request, *args, **kwargs):
        vipCardId = request.data
        if vipCardId:
            try:
                instance = self.queryset.filter(id=vipCardId).first()
                if instance:
                    instance.isDel = 1
                    instance.save()
                    return SuccessResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='会员卡不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class UserVipCardModelViewSet(CustomModelViewSet):
    """
    用户会员卡管理 的CRUD视图
    """
    queryset = UserVip.objects.filter(isDel=0)
    serializer_class = UserVipCardSerializer
    filter_class = UserVipCardFilter
    ordering = 'create_datetime'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_user_vip(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            userVipObj = self.queryset.filter(user_id=jsonData.get('userId')).filter(vipCard_id=jsonData.get('vipCardId')).first()
            if userVipObj:
                return ErrorResponse(msg='该用户已存在会员卡')
            serializer = UserVipCardSerializer(data=jsonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            instance = serializer.data.get('id')
            instance.user_id = jsonData.get('userId')
            instance.vipCard_id = jsonData.get('vipCardId')
            instance.save()
            return SuccessResponse(msg='新增成功')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_user_vip(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(jsonData.get('id')).first()
                if instance:
                    instance.vipCard_id = jsonData.get('vipCardId')
                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                else:
                    return ErrorResponse(msg='用户会员卡不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class ExchangeModelViewSet(CustomModelViewSet):
    """
    交易所管理 的CRUD视图
    """
    queryset = Exchange.objects.filter(isDel=0)
    serializer_class = ExchangeSerializer
    filter_class = ExchangeFilter
    ordering = 'create_datetime'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_exchange(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            try:
                exchangeObj = self.queryset.filter(name=jsonData.get('name')).first()
                if exchangeObj:
                    return ErrorResponse(msg='交易所已存在')
                serializer = ExchangeSerializer(data=jsonData)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return SuccessResponse(msg='新增成功')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_exchange(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(id=jsonData.get('id')).first()
                if instance:
                    instance.name = jsonData.get('name')
                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                else:
                    return ErrorResponse(msg='交易所不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    def del_exchange(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(jsonData.get('id')).first()
                if instance:
                    instance.isDel = jsonData.get('isDel')
                    instance.save()
                    return SuccessResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='交易所不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class UserExchangeConfigModelViewSet(CustomModelViewSet):
    """
    用户交易所管理 的CRUD视图
    """
    queryset = UserExchangeConfig.objects.filter(isDel=0)
    serializer_class = UserExchangeConfigSerializer
    filter_class = UserExchangeConfigFilter
    ordering = 'create_datetime'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_user_exchange(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            exchangeObj = self.queryset.filter(user_id=jsonData.get('exchangeId')).first()
            if exchangeObj:
                return ErrorResponse(msg='用户交易所已存在')
            serializer = UserExchangeConfigSerializer(data=jsonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            instance = serializer.data.get('id')
            instance.user_id = jsonData.get('userId')
            instance.exchange_id = jsonData.get('exchangeId')
            instance.save()
            return SuccessResponse(msg='新增成功')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_user_exchange(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(jsonData.get('id')).first()
                if instance:
                    instance.exchange_id = jsonData.get('exchangeId')
                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                else:
                    return ErrorResponse(msg='用户交易所不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    def del_user_exchange(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(jsonData.get('id')).first()
                if instance:
                    instance.isDel = jsonData.get('isDel')
                    instance.save()
                    return SuccessResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='用户交易所不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class RobotModelViewSet(CustomModelViewSet):
    """
    机器人管理 的CRUD视图
    """
    queryset = Robot.objects.filter(isDel=0)
    serializer_class = RobotSerializer
    filter_class = RobotFilter
    ordering = 'create_datetime'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_robot(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            try:
                robotObj = self.queryset.filter(id=jsonData.get('robotId')).first()
                if robotObj:
                    return ErrorResponse(msg='机器人已存在')
                serializer = RobotSerializer(data=jsonData)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return SuccessResponse(msg='新增成功')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_robot(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(id=jsonData.get('id')).first()
                if instance:
                    instance.originAmount = jsonData.get('originAmount')
                    instance.vipAmount = jsonData.get('vipAmount')
                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                else:
                    return ErrorResponse(msg='机器人不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    def del_robot(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(jsonData.get('id')).first()
                if instance:
                    instance.isDel = jsonData.get('isDel')
                    instance.save()
                    return SuccessResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='机器人不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class UserRobotModelViewSet(CustomModelViewSet):
    """
    用户机器人管理 的CRUD视图
    """
    queryset = UserRobot.objects.filter(isDel=0)
    serializer_class = UserRobotSerializer
    filter_class = UserRobotFilter
    ordering = 'create_datetime'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_user_robot(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            userRobotObj = self.queryset.filter(robot_id=jsonData.get('userRobotId')).first()
            if userRobotObj:
                return ErrorResponse(msg='用户机器人已存在')
            serializer = UserRobotSerializer(data=jsonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return SuccessResponse(msg='新增成功')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_user_robot(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(id=jsonData.get('id')).first()
                if instance:
                    instance.robot_id = jsonData.get('robotId')
                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                else:
                    return ErrorResponse(msg='用户机器人不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    def del_robot(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(jsonData.get('id')).first()
                if instance:
                    instance.isDel = jsonData.get('isDel')
                    instance.save()
                    return SuccessResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='用户机器人不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')
