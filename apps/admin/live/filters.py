import django_filters
from django.contrib.auth import get_user_model

from apps.admin.live.models import Tags, Lives


class TagsFilter(django_filters.rest_framework.FilterSet):
    """
    tags 简单序过滤器
    """

    class Meta:
        model = Tags
        fields = '__all__'


class LivesFilter(django_filters.rest_framework.FilterSet):
    """
    直播间 简单序过滤器
    """

    class Meta:
        model = Lives
        fields = '__all__'
