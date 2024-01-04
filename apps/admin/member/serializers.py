from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.admin.member.models.userExchangeConfig import Exchange
from apps.admin.op_drf.serializers import CustomModelSerializer
from apps.admin.op_drf.validator import CustomUniqueValidator
from apps.admin.member.models import VipCard, UserVip, UserExchangeConfig, Robot, UserRobot

UserProfile = get_user_model()

# ================================================= #
# ************** 用户管理 序列化器  ************** #
# ================================================= #


class MemberSerializer(CustomModelSerializer):
    """
    简单用户序列化器
    """

    class Meta:
        model = UserProfile
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'creator','date_joined', 'dept_belong_id', 'first_name', 'last_name',
                   'is_staff')


class ExportUserProfileSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name', 'email', 'mobile', 'gender', 'is_active', 'last_login')


class VipCardSerializer(CustomModelSerializer):
    """
    简单会员卡序列化器
    """

    class Meta:
        model = VipCard
        fields = '__all__'


class UserVipCardSerializer(CustomModelSerializer):
    """
    简单用户会员卡序列化器
    """
    user = serializers.CharField()
    vipCard = serializers.CharField()

    class Meta:
        model = UserVip
        fields = '__all__'


class ExchangeSerializer(CustomModelSerializer):
    """
    简单交易所序列化器
    """

    class Meta:
        model = Exchange
        fields = '__all__'


class UserExchangeConfigSerializer(CustomModelSerializer):
    """
    简单用户交易所序列化器
    """
    user = serializers.CharField(read_only=True)
    exchange = serializers.CharField(read_only=True)

    class Meta:
        model = UserExchangeConfig
        fields = '__all__'


class RobotSerializer(CustomModelSerializer):
    """
    简单机器人序列化器
    """

    class Meta:
        model = Robot
        fields = '__all__'


class UserRobotSerializer(CustomModelSerializer):
    """
    简单用户机器人序列化器
    """
    user = serializers.CharField(read_only=True)
    exchange = serializers.CharField(read_only=True)

    class Meta:
        model = UserRobot
        fields = '__all__'
