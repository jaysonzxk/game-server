import base64
import hashlib
import json
import logging
import re
import string
from random import choice
import calendar
import time
from django.utils.translation import gettext as _

from captcha.models import CaptchaStore
from captcha.views import captcha_image
from channels.auth import login
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_simplejwt.views import TokenRefreshView

from application.settings import REGEX_MOBILE
from apps.admin.permission.serializers import UserProfileSerializer
from apps.admin.system.models import LoginInfor
from apps.app.utils.request_util import get_request_ip, get_login_location, get_os
from apps.app.utils.jwt_util import jwt_get_session_id
from rest_framework_simplejwt.tokens import RefreshToken

from application import dispatch
from apps.admin.permission.models import UserProfile
from apps.app.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from apps.app.utils.request_util import save_login_log
from apps.app.utils.serializers import CustomModelSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


class LogoutView(APIView):
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)
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


class AppLoginView(ObtainJSONWebToken):
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

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        key = None
        token = None
        _dict = {}
        if data:
            if data.get('loginType') == 0:
                if data.get('mobile'):
                    if cache.get(data.get('mobile')) is None:
                        return ErrorResponse(msg=_('验证码已失效'))
                    if str(data.get('code')) != json.loads(cache.get(data.get('mobile'))).get('code'):
                        return ErrorResponse(msg=_('验证码错误'))
                    try:
                        user = UserProfile.objects.filter(mobile=data.get('mobile')).first()
                        if user:
                            try:
                                userObj = UserProfile.objects.filter(mobile=data.get('mobile')).first()
                                data["name"] = userObj.name
                                data["userId"] = userObj.id
                                data["avatar"] = userObj.avatar
                                data['user_type'] = userObj.user_type
                                data['mobile'] = userObj.mobile
                                data['email'] = userObj.email
                            except Exception as e:
                                return ErrorResponse(msg=_('参数错误'))
                        else:
                            del data['code']
                            data['user_type'] = 1
                            data['username'] = data.get('mobile')
                            import random
                            data['name'] = data.get('mobile')
                            inviteCode = ''.join(random.sample(string.ascii_letters + string.digits, 6))
                            data['inviteCode'] = inviteCode.upper()  # 邀请码
                            serializer = UserProfileSerializer(data=data)
                            if serializer.is_valid(raise_exception=True):
                                serializer.save()
                            try:
                                userObj = UserProfile.objects.filter(mobile=data.get('mobile')).first()
                                data["name"] = userObj.name
                                data["userId"] = userObj.id
                                data["avatar"] = userObj.avatar
                                data['user_type'] = userObj.user_type
                                data['mobile'] = userObj.mobile
                                data['email'] = userObj.email
                            except Exception as e:
                                return ErrorResponse(msg=_('参数错误'))
                        payload = jwt_payload_handler(userObj)
                        token = jwt_encode_handler(payload)
                        _dict = {'id': userObj.id, 'mobile': userObj.mobile, 'email': userObj.email, 'token': token}
                        session_id = jwt_get_session_id(token)
                        key = f"{self.prefix}_{session_id}_{userObj.username}"
                        # 单点登录
                        last_token = cache.get(key)
                        if last_token:
                            cache.delete(key)
                        cache.set(key, json.dumps(_dict), 2592000)  # 一个月到期
                        res = {'token': token}
                        self.save_login_infor(request, '登录成功', session_id=session_id)
                        return DetailResponse(data=res)
                    except Exception as e:
                        return ErrorResponse(msg=_('未知错误'))
            if data.get('loginType') == 1:
                from apps.app.utils.encryption import encode_password
                if data.get('username'):
                    try:
                        userObj = UserProfile.objects.filter(username=data.get('username'))
                        if not userObj.exists():
                            return ErrorResponse(msg=_('账号不存在'))
                        else:
                            password1 = userObj.first().password
                            password2 = encode_password(data.get('password'))
                            if password1 != password2:
                                return ErrorResponse(msg='账号或密码错误')
                            payload = jwt_payload_handler(userObj.first())
                            token = jwt_encode_handler(payload)
                            _dict = {'id': userObj.first().id, 'mobile': userObj.first().mobile,
                                     'email': userObj.first().email, 'token': token}
                            session_id = jwt_get_session_id(token)
                            key = f"{self.prefix}_{session_id}_{userObj.first().username}"
                            # 单点登录
                            last_token = cache.get(key)
                            if last_token:
                                cache.delete(key)
                            cache.set(key, json.dumps(_dict), 2592000)  # 一个月到期
                            res = {'token': token}
                            self.save_login_infor(request, '登录成功', session_id=session_id)
                            return DetailResponse(data=res, msg=_('登录成功'))
                    except Exception as e:
                        return ErrorResponse(msg=_('未知错误'))
            else:
                return ErrorResponse(msg=_('参数错误'))
        return ErrorResponse(msg=_('参数错误'))


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

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ["username", "password"]


class ApiLogin(APIView):
    """接口文档的登录接口"""

    serializer_class = ApiLoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user_obj = auth.authenticate(
            request,
            username=username,
            password=hashlib.md5(password.encode(encoding="UTF-8")).hexdigest(),
        )
        if user_obj:
            login(request, user_obj)
            return redirect("/")
        else:
            return ErrorResponse(msg="账号/密码错误")


class GetPhoneCode(APIView):
    """
    获取验证码
    """
    authentication_classes = []
    permission_classes = []

    # 生成随机验证码的函数
    def generate_code(self):
        seeds = "1234567890"
        code_lst = []
        for i in range(4):
            code_lst.append(choice(seeds))
        return "".join(code_lst)

    def verify_phone(self, mobile):
        return re.match(REGEX_MOBILE, mobile)

    def verify_times(self, mobile):
        now_time = calendar.timegm(time.gmtime())
        if cache.get(mobile):
            if now_time - json.loads(cache.get(mobile)).get('utc_time') <= 60:
                return False

    def get(self, request: Request, *args, **kwargs):
        mobile = request.query_params.get('mobile')
        key = mobile
        utc_time = calendar.timegm(time.gmtime())
        code = {
            'code': self.generate_code(),
            'utc_time': utc_time
        }
        if mobile:
            if self.verify_times(mobile) is False:
                return ErrorResponse(msg=_('请求频繁,请稍后重试'))
            if self.verify_phone(mobile) is None:
                return ErrorResponse(msg=_('手机号格式不正确'))
            else:
                cache.set(key, json.dumps(code), 300)
        else:
            return ErrorResponse(msg=_('参数错误'))
        return DetailResponse(data=code, msg=_('发送成功'))
