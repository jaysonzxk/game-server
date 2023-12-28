from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.app.robot.views import UserRobotModelViewSet

router = DefaultRouter()
# router.register(r'userRobot', UserRobotModelViewSet)
urlpatterns = [
    re_path('changeStatus', UserRobotModelViewSet.as_view({'post':  'change_robot'}))
]
urlpatterns += router.urls
