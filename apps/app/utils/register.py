import base64
import binascii
import datetime
import hashlib
import json
import logging
import os
import random
import string
from uuid import uuid4
from django.utils.translation import gettext as _

from captcha.models import CaptchaStore
from captcha.views import captcha_image
from channels.auth import login
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.admin.system.models import LoginInfor
from apps.admin.utils.jwt_util import jwt_get_session_id, jwt_response_payload_handler
from rest_framework_simplejwt.tokens import RefreshToken

from application import dispatch
from apps.admin.permission.models import UserProfile
from apps.admin.permission.serializers import UserProfileSerializer
from apps.app.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from apps.app.utils.request_util import get_request_ip, get_login_location, get_os
from apps.app.utils.serializers import CustomModelSerializer
from apps.app.utils.encryption import encode_password


logger = logging.getLogger(__name__)

User = get_user_model()


class CaptchaView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={"200": openapi.Response("获取成功")},
        security=[],
        operation_id="captcha-get",
        operation_description="验证码获取",
    )
    def get(self, request):
        data = {}
        if dispatch.get_system_config_values("base.captcha_state"):
            hash_key = CaptchaStore.generate_key()
            _id = CaptchaStore.objects.filter(hashkey=hash_key).first().id
            image = captcha_image(request, hash_key)
            # 将图片转换为base64
            image_base = base64.b64encode(image.content)
            data = {
                "key": _id,
                "image_base": "data:image/png;base64," + image_base.decode("utf-8"),
            }
        return DetailResponse(data=data)


class LogoutView(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX', 'JWT')

    def post(self, request):
        user = request.user
        res = UserProfile.objects.filter(username=user.username, password=user.password).first()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(res)
        token = jwt_encode_handler(payload)
        session_id = jwt_get_session_id(token)
        key = f"{self.prefix}_{session_id}_{res.username}"
        cache.delete(key)
        return SuccessResponse()


class RegisterView(ObtainJSONWebToken):
    """
    账号密码注册
    """
    JWT_AUTH_COOKIE = ''
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX')
    ex = settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA')

    def save_login_infor(self, request, msg='', status=True, session_id=''):
        User = get_user_model()
        instance = LoginInfor()
        instance.session_id = session_id
        # instance.browser = get_browser(request)
        instance.ipaddr = get_request_ip(request)
        instance.loginLocation = get_login_location(request)
        instance.msg = msg
        instance.os = get_os(request)
        instance.status = status
        instance.creator = request.user and User.objects.filter(username=request.data.get('username')).first()
        instance.save()

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        jsonData = request.data
        try:
            if jsonData:
                user = UserProfile.objects.filter(
                    Q(username=jsonData.get('username')) | Q(mobile=jsonData.get('mobile')))
                if user.exists():
                    return ErrorResponse(msg=_('用户名或手机号已存在'))
                password = encode_password(jsonData.get('password'))
                inviteCode = ''.join(random.sample(string.ascii_letters + string.digits, 6))
                data = {'inviteCode': inviteCode.upper(), 'user_type': 1, 'username': jsonData.get('username'),
                        'mobile': jsonData.get('mobile'), 'name': jsonData.get('username'), 'balance': 0}
                serializer = UserProfileSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                instance = UserProfile.objects.filter(username=jsonData.get('username')).first()
                instance.password = password
                instance.save()

                # 缓存token
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user.first())
                token = jwt_encode_handler(payload)
                response_data = jwt_response_payload_handler(token, user.first(), request)
                response = DetailResponse(response_data, msg=_('注册成功'))
                _dict = {'id': user.first().id, 'username': user.first().username, 'token': token}
                session_id = jwt_get_session_id(token)
                key = f"{self.prefix}_{session_id}_{user.first().username}"
                last_token = cache.get(key)
                if last_token:
                    cache.delete(key)
                cache.set(key, json.dumps(_dict), 2592000)  # 一个月到期
                # res = {'access': token, **data}
                self.save_login_infor(request, '注册成功', session_id=session_id)
                return response
        except Exception as e:
            return ErrorResponse(msg=_('未知错误'))


class CustomTokenRefreshView(TokenRefreshView):
    """
    自定义token刷新
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            data = {
                "access": str(token.access_token),
                "refresh": str(token)
            }
        except:
            return ErrorResponse(status=HTTP_401_UNAUTHORIZED)
        return DetailResponse(data=data)


class ApiLoginSerializer(CustomModelSerializer):
    """接口文档登录-序列化器"""

    # username = serializers.CharField()
    # password = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ["username", "password"]


class ApiLogin(APIView):
    """接口文档的登录接口"""

    serializer_class = ApiLoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        if request:
            # login(request, user_obj)
            return redirect("/")
        # username = request.data.get("username")
        # password = request.data.get("password")
        # user_obj = auth.authenticate(
        #     request,
        #     username=username,
        #     password=hashlib.md5(password.encode(encoding="UTF-8")).hexdigest(),
        # )
        # if user_obj:
        #     login(request, user_obj)
        #     return redirect("/")
        # else:
        #     return ErrorResponse(msg="账号/密码错误")
