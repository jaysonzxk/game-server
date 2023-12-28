import json
import os
import sys
from urllib.parse import urlsplit

# from werkzeug.utils import secure_filename

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.views import APIView

from application import settings
from apps.admin.op_drf.response import ErrorResponse, SuccessResponse
from apps.admin.utils.string_util import uuid


class ImageUploadView(APIView):
    """
    图片上传接口
    """
    authentication_classes = []
    permission_classes = []

    # parser_classes = [FormParser, MultiPartParser]

    def save_path(self, filename):

        ext = str(filename).split('.')[-1]
        filename = f'{uuid().hex[:10]}.{ext}'
        images = os.path.join('pay', filename)
        save_path = os.path.join(settings.MEDIA_ROOT, images)
        return save_path

    def post(self, request: Request):
        image = request.FILES.get('file')
        # 判断获取请求的是http还是https
        http = urlsplit(request.build_absolute_uri(None)).scheme
        host = request.META['HTTP_HOST']
        # 获取当前域名
        shorturl = http + '://' + host
        data = {}
        if image == 'None' or image == '' or image is None:
            return ErrorResponse(msg='上传图片不能为空')
        elif str(image).split('.')[1] in settings.ALLOWED_IMG_TYPE:
            save_image_path = self.save_path(image)
            with open(save_image_path, 'wb') as f:
                f.write(image.read())
            if '\\' in save_image_path:
                image_url = os.path.join(shorturl, '/'.join(save_image_path.split('\\')[3:6])).replace('\\', '/')
            else:
                image_url = os.path.join(shorturl, '/'.join(
                    save_image_path.split('/')[len(save_image_path.split('/'))-3:]))
            data['image'] = image_url
            return SuccessResponse(data=data)
        else:
            return ErrorResponse(msg='图片格式错误')
