from django.contrib.auth import authenticate, get_user_model
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.op_drf.response import SuccessResponse, ErrorResponse
from apps.admin.op_drf.filters import DataLevelPermissionsFilter
from apps.admin.op_drf.viewsets import CustomModelViewSet
from apps.admin.live.filters import TagsFilter, LivesFilter
from apps.admin.live.serializers import TagsSerializer, LivesSerializer
from apps.admin.live.models import Tags, Lives
from apps.admin.utils.json_response import DetailResponse


class TagsModelViewSet(CustomModelViewSet):
    """
    Tags 的CRUD视图
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    filter_class = TagsFilter
    ordering = 'sort'  # 默认排序

    @transaction.atomic
    def add_tag(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            tagObj = self.queryset.filter(name=jsonData.get('name'))
            if tagObj.exists():
                return ErrorResponse(msg='该tag已存在')
            try:
                serializer = TagsSerializer(data=jsonData)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return SuccessResponse(msg='新增成功')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_tag(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(id=jsonData.get('id')).first()
                if instance:
                    instance.name = jsonData.get('name')
                    instance.sort = jsonData.get('sort')

                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                return ErrorResponse(msg='tag不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def del_tag(self, request: Request, *args, **kwargs):
        tagId = request.data
        if tagId:
            try:
                instance = self.queryset.filter(id=tagId).first()
                if instance:
                    instance.isDel = 1
                    instance.save()
                    return SuccessResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='tag不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class LivesModelViewSet(CustomModelViewSet):
    """
    直播间 CRUD视图
    """
    queryset = Lives.objects.all()
    serializer_class = LivesSerializer
    filter_class = LivesFilter
    ordering = 'sort'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_live(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            liveObj = self.queryset.filter(tag_id=jsonData.get('tag')).filter(
                name=jsonData.get('name'))
            if liveObj.exists():
                return ErrorResponse(msg='该直播间已存在')
            serializer = LivesSerializer(data=jsonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return DetailResponse(msg='新增成功')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_live(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(jsonData.get('id')).first()
                if instance:
                    instance.tag_id = jsonData.get('tag')
                    instance.status = jsonData.get('status')
                    instance.name = jsonData.get('name')
                    instance.uri = jsonData.get('uri')
                    instance.sort = jsonData.get('sort')
                    instance.heatValue = jsonData.get('heatValue')
                    instance.tag_id = jsonData.get('tag')
                    instance.tickets = jsonData.get('tickets')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                else:
                    return ErrorResponse(msg='直播间不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    def delete_live(self, request: Request, *args, **kwargs):
        liveId = request.data
        if liveId:
            try:
                instance = self.queryset.filter(id=liveId)
                if instance.exists():
                    instance.first().isDel = 1
                    instance.first().save()
                    return DetailResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='直播间不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    def get_all_tag(self, request: Request, *args, **kwargs):
        try:
            results = Tags.objects.values('id', 'name')
            return DetailResponse(data=results)
        except Exception as e:
            return ErrorResponse(msg='未知异常')
