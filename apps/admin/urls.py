"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from captcha.conf import settings as ca_settings
from captcha.helpers import captcha_image_url, captcha_audio_url
from captcha.models import CaptchaStore
from django.conf.urls import url
from django.urls import re_path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.views import APIView

from apps.admin.permission.views import GetUserProfileView, GetRouters
from apps.admin.utils.login import LoginView, LogoutView
from apps.admin.op_drf.response import SuccessResponse
from apps.admin.utils.upload import ImageUploadView


class CaptchaRefresh(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        new_key = CaptchaStore.pick()
        to_json_response = {
            "key": new_key,
            "image_url": captcha_image_url(new_key),
            "audio_url": captcha_audio_url(new_key) if ca_settings.CAPTCHA_FLITE_PATH else None,
        }
        return SuccessResponse(to_json_response)


urlpatterns = [
    re_path('api-token-auth/', LoginView.as_view(), name='api_token_auth'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^login', LoginView.as_view()),
    re_path(r'^logout/$', LogoutView.as_view()),
    re_path(r'^getInfo/$', GetUserProfileView.as_view()),
    re_path(r'^getRouters/$', GetRouters.as_view()),
    url(r"captcha/refresh/$", CaptchaRefresh.as_view(), name="captcha-refresh"),  # 刷新验证码
    re_path('captcha/', include('captcha.urls')),  # 图片验证码 路由
    re_path(r'^permission/', include('apps.admin.permission.urls')),
    re_path(r'^system/', include('apps.admin.system.urls')),
    re_path(r'^celery/', include('apps.admin.celery.urls')),
    re_path(r'^monitor/', include('apps.admin.monitor.urls')),
    re_path(r'^pay/', include('apps.admin.pay.urls')),
    re_path(r'^games/', include('apps.admin.game.urls')),
    re_path(r'^live/', include('apps.admin.live.urls')),
    # 用户
    re_path(r'^member/', include('apps.admin.member.urls')),
    re_path(r'^upload', ImageUploadView.as_view())
]