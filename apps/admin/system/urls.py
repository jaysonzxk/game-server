from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.admin.system.views import DictDataModelViewSet, DictDetailsModelViewSet, \
    ConfigSettingsModelViewSet, SaveFileModelViewSet, MessagePushModelViewSet, LoginInforModelViewSet, \
    OperationLogModelViewSet, CeleryLogModelViewSet, SystemInfoApiView, BannersModelViewSet, AnnouncementModelViewSet, MarqueeModelViewSet

router = DefaultRouter()
router.register(r'dict/type', DictDataModelViewSet)
router.register(r'dict/data', DictDetailsModelViewSet)
router.register(r'config', ConfigSettingsModelViewSet)
router.register(r'savefile', SaveFileModelViewSet)
router.register(r'message', MessagePushModelViewSet)
router.register(r'logininfor', LoginInforModelViewSet)
router.register(r'operation_log', OperationLogModelViewSet)
router.register(r'celery_log', CeleryLogModelViewSet)
router.register(r'banners', BannersModelViewSet)
router.register(r'announcement', AnnouncementModelViewSet)
router.register(r'marquee', MarqueeModelViewSet)

urlpatterns = [
    re_path('dict/get/type/(?P<pk>.*)/', DictDetailsModelViewSet.as_view({'get': 'dict_details_list'})),
    re_path('config/configKey/(?P<pk>.*)/', ConfigSettingsModelViewSet.as_view({'get': 'get_config_key'})),
    # 参数管理导出
    re_path('config/export/', ConfigSettingsModelViewSet.as_view({'get': 'export'})),
    # 清理参数缓存
    re_path('config/clearCache/', ConfigSettingsModelViewSet.as_view({'delete': 'clearCache', })),
    # 导出字典管理数据
    re_path('dict/type/export/', DictDataModelViewSet.as_view({'get': 'export'})),
    # 导出字典详情数据
    re_path('dict/data/export/', DictDetailsModelViewSet.as_view({'get': 'export'})),
    # 清理字典缓存
    re_path('dict/type/clearCache/', DictDetailsModelViewSet.as_view({'delete': 'clearCache', })),
    # 消息通知导出
    re_path('message/export/', MessagePushModelViewSet.as_view({'get': 'export', })),
    # 用户个人消息列表
    re_path('message/user_messages/', MessagePushModelViewSet.as_view({'get': 'get_user_messages', })),
    # 改为已读
    re_path('message/is_read/(?P<pk>.*)/', MessagePushModelViewSet.as_view({'put': 'update_is_read', })),
    # 清空操作日志
    re_path('operation_log/clean/', OperationLogModelViewSet.as_view({'delete': 'clean_all', })),
    # 导出操作日志
    re_path('operation_log/export/', OperationLogModelViewSet.as_view({'get': 'export', })),
    # 清空登录日志
    re_path('logininfor/clean/', LoginInforModelViewSet.as_view({'delete': 'clean_all', })),
    # 导出登录日志
    re_path('logininfor/export/', LoginInforModelViewSet.as_view({'get': 'export', })),
    # 清空定时日志
    re_path('celery_log/clean/', CeleryLogModelViewSet.as_view({'delete': 'clean_all', })),
    # 导出定时日志
    re_path('celery_log/export/', CeleryLogModelViewSet.as_view({'get': 'export', })),
    # 清除废弃文件
    re_path('clearsavefile/', SaveFileModelViewSet.as_view({'post': 'clearsavefile', })),
    # 获取系统信息cpu、内存、硬盘
    re_path('sys/info/', SystemInfoApiView.as_view()),
    # 公告
    re_path('announcement/add/', AnnouncementModelViewSet.as_view({'post': 'add_announcement'})),
    re_path('announcement/update/', AnnouncementModelViewSet.as_view({'post': 'update_announcement'})),
    re_path('announcement/del/', AnnouncementModelViewSet.as_view({'post': 'del_announcement'})),
    # 跑马灯
    re_path('marquee/add/', MarqueeModelViewSet.as_view({'post': 'add_marquee'})),
    re_path('marquee/update/', MarqueeModelViewSet.as_view({'post': 'update_marquee'})),
    re_path('marquee/del/', MarqueeModelViewSet.as_view({'post': 'del_marquee'})),
    # 轮播图
    re_path('banners/add', BannersModelViewSet.as_view({'post': 'add_banner'})),
    re_path('banners/update', BannersModelViewSet.as_view({'post': 'update_banner'})),
    re_path('banners/del', BannersModelViewSet.as_view({'post': 'de_banners'}))

]
urlpatterns += router.urls
