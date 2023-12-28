from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.app.mine.views import UserModelViewSet, RobotModelViewSet, PayChannelModelViewSet, PromotionModelViewSet
from apps.app.mine.vip.views import ByVipModelViewSet, VipModelViewSet
from apps.app.mine.wallet.views import AmountConfigModelViewSet

router = DefaultRouter()
# router.register(r'user', UserModelViewSet)
urlpatterns = [
    re_path('info', UserModelViewSet.as_view({'get': 'user_info'})),
    # 会员卡接口
    # 会员卡列表
    re_path('vipCard/list', VipModelViewSet.as_view({'get': 'get_vip_list'})),
    # 购买VIP
    re_path('buy/vip', ByVipModelViewSet.as_view({'post': 'buy_vip'})),

    # 钱包接口
    re_path('wallet/amonut/list', AmountConfigModelViewSet.as_view({'get': 'get_amount_list'})),


    re_path('robot/list', RobotModelViewSet.as_view({'get': 'get_robot_list'})),
    re_path('channel/list', PayChannelModelViewSet.as_view({'get': 'get_channel_list'})),
    # 推广列表
    re_path('promotion/list', PromotionModelViewSet.as_view({'get': 'get_promotion_list'})),

]
urlpatterns += router.urls
