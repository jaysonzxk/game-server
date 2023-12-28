from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.admin.member.views import UserProfileModelViewSet, VipCardModelViewSet, UserVipCardModelViewSet, \
    ExchangeModelViewSet, UserExchangeConfigModelViewSet, RobotModelViewSet, UserRobotModelViewSet

router = DefaultRouter()
router.register(r'user', UserProfileModelViewSet)
router.register(r'vipCard', VipCardModelViewSet)
router.register(r'userVip', UserVipCardModelViewSet)
router.register(r'exchange', ExchangeModelViewSet)
router.register(r'userExchange', UserExchangeConfigModelViewSet)
router.register(r'robot', RobotModelViewSet)
router.register(r'userRobot', UserRobotModelViewSet)
urlpatterns = [

    # 更新状态
    re_path('user/changeStatus/', UserProfileModelViewSet.as_view({'put': 'change_status'})),
    # 获取用户详情
    re_path('user/details/', UserProfileModelViewSet.as_view({'get': 'get_user_details'})),
    # 获取、更新用户个人信息
    re_path('user/profile/', UserProfileModelViewSet.as_view({'get': 'profile', 'put': 'put_profile'})),

    # 会员卡
    re_path('vipCard/add/', VipCardModelViewSet.as_view({'post': 'add_vip_card'})),
    re_path('vipCard/update/', VipCardModelViewSet.as_view({'post': 'update_vip_card'})),
    re_path('vipCard/del/', VipCardModelViewSet.as_view({'post': 'del_vip_card'})),

    # 用户会员卡
    re_path('userVip/add/', UserVipCardModelViewSet.as_view({'post': 'add_user_vip'})),
    re_path('userVip/update/', UserVipCardModelViewSet.as_view({'post': 'update_user_vip'})),

    # 交易所
    re_path('exchange/add/', ExchangeModelViewSet.as_view({'post': 'add_exchange'})),
    re_path('exchange/update/', ExchangeModelViewSet.as_view({'post': 'update_exchange'})),
    re_path('exchange/del/', ExchangeModelViewSet.as_view({'post': 'del_exchange'})),

    # 用户交易所
    re_path('userExchange/add/', UserExchangeConfigModelViewSet.as_view({'post': 'add_user_exchange'})),
    re_path('userExchange/update/', UserExchangeConfigModelViewSet.as_view({'post': 'update_user_exchange'})),
    re_path('userExchange/del/', UserExchangeConfigModelViewSet.as_view({'post': 'del_user_exchange'})),

    # 机器人
    re_path('robot/add/', RobotModelViewSet.as_view({'post': 'add_robot'})),
    re_path('robot/update/', RobotModelViewSet.as_view({'post': 'update_robot'})),
    re_path('robot/del/', RobotModelViewSet.as_view({'post': 'del_robot'})),

    # 用户机器人
    re_path('userRobot/update', UserRobotModelViewSet.as_view({'post': 'update_user_robot'}))
]
urlpatterns += router.urls
