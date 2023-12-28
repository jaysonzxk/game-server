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
from rest_framework.views import APIView

from apps.app.utils.login import LogoutView, AppLoginView, GetPhoneCode
from apps.app.op_drf.response import SuccessResponse
from apps.app.utils.upload import ImageUploadView


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
    # re_path('api-token-auth/', LoginView.as_view(), name='api_token_auth'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework1')),
    re_path(r'^login$', AppLoginView.as_view()),
    re_path(r'^logout/$', LogoutView.as_view()),
    re_path(r'^getCode$', GetPhoneCode.as_view()),
    # 首页
    re_path(r'^home/', include('apps.app.home.urls')),
    re_path(r'^robot/', include('apps.app.robot.urls')),
    re_path(r'^order/', include('apps.app.order.urls')),
    re_path(r'^mine/', include('apps.app.mine.urls')),

    # 图片上传
    re_path(r'^upload', ImageUploadView.as_view())
]
