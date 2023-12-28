from django.contrib.auth import authenticate, get_user_model
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db import transaction

from apps.admin.op_drf.response import SuccessResponse, ErrorResponse
from apps.admin.op_drf.filters import DataLevelPermissionsFilter
from apps.admin.op_drf.viewsets import CustomModelViewSet
from apps.admin.game.filters import GameCategoryFilter, GameManufacturerFilter, GamesFilter
from apps.admin.game.serializers import GameCategorySerializer, GameManufacturerSerializer, GamesSerializer
from apps.admin.game.models import GameCategory, GameManufacturer, Games


class GameCategoryModelViewSet(CustomModelViewSet):
    """
    游戏大类 的CRUD视图
    """
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    filter_class = GameCategoryFilter
    ordering = 'sort'  # 默认排序

    @transaction.atomic
    def add_category(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            vipObj = self.queryset.filter(name=jsonData.get('name')).first()
            if vipObj:
                return ErrorResponse(msg='该游戏分类已存在')
            serializer = GameManufacturerSerializer(data=jsonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return SuccessResponse(msg='新增成功')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_category(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(id=jsonData.get('id')).first()
                if instance:
                    instance.name = jsonData.get('name')
                    instance.image = jsonData.get('image')
                    instance.sort = jsonData.get('sort')
                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                return ErrorResponse(msg='游戏分类不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def del_category(self, request: Request, *args, **kwargs):
        categoryId = request.data
        if categoryId:
            try:
                instance = self.queryset.filter(id=categoryId).first()
                if instance:
                    instance.isDel = 1
                    instance.save()
                    return SuccessResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='游戏分类不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class GameManufacturerViewSet(CustomModelViewSet):
    """
    游戏厂商 的CRUD视图
    """
    queryset = GameManufacturer.objects.all()
    serializer_class = GameManufacturerSerializer
    filter_class = GameManufacturerFilter
    ordering = 'sort'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_manufacturer(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            vipObj = self.queryset.filter(name=jsonData.get('name')).first()
            if vipObj:
                return ErrorResponse(msg='该厂商已存在')
            serializer = GameManufacturerSerializer(data=jsonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return SuccessResponse(msg='新增成功')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_manufacturer(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(id=jsonData.get('id')).first()
                if instance:
                    instance.name = jsonData.get('name')
                    instance.gameCategory_id = jsonData.get('gameCategoryId')
                    instance.image = jsonData.get('image')
                    instance.sort = jsonData.get('sort')
                    instance.status = jsonData.get('status')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                return ErrorResponse(msg='游戏厂商不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def del_manufacturer(self, request: Request, *args, **kwargs):
        manufacturerId = request.data
        if manufacturerId:
            try:
                instance = self.queryset.filter(id=manufacturerId).first()
                if instance:
                    instance.isDel = 1
                    instance.save()
                    return SuccessResponse(msg='删除成功')
                else:
                    return ErrorResponse(msg='游戏厂商不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')


class GamesModelViewSet(CustomModelViewSet):
    """
    游戏 的CRUD视图
    """
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    filter_class = GamesFilter
    ordering = 'sort'  # 默认排序

    @transaction.atomic  # 加事务回滚
    def add_games(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData:
            userVipObj = self.queryset.filter(user_id=jsonData.get('userId')).filter(
                vipCard_id=jsonData.get('vipCardId')).first()
            if userVipObj:
                return ErrorResponse(msg='该游戏已存在')
            serializer = GamesSerializer(data=jsonData)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            instance = serializer.data.get('id')
            instance.gameManufacturer_id = jsonData.get('gameManufacturerId')
            instance.save()
            return SuccessResponse(msg='新增成功')
        return ErrorResponse(msg='参数错误')

    @transaction.atomic
    def update_games(self, request: Request, *args, **kwargs):
        jsonData = request.data
        if jsonData and jsonData.get('id'):
            try:
                instance = self.queryset.filter(jsonData.get('id')).first()
                if instance:
                    instance.gameManufacturer_id = jsonData.get('gameManufacturerId')
                    instance.status = jsonData.get('status')
                    instance.name = jsonData.get('name')
                    instance.image = jsonData.get('image')
                    instance.url = jsonData.get('url')
                    instance.sort = jsonData.get('sort')
                    instance.isRecommend = jsonData.get('isRecommend')
                    instance.isHot = jsonData.get('isHot')
                    instance.save()
                    return SuccessResponse(msg='修改成功')
                else:
                    return ErrorResponse(msg='游戏不存在')
            except Exception as e:
                return ErrorResponse(msg='未知错误')
        return ErrorResponse(msg='参数错误')
