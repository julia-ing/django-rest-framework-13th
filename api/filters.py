from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from taggit.models import Tag
from api.models import *


class PostFilter(FilterSet):
    text = filters.CharFilter(field_name='text', lookup_expr='icontains')
    tags = filters.CharFilter(method='filter_by_tags')

    class Meta:
        model = Post
        fields = ['writer', 'text', 'tags', 'can_comment']

    def filter_by_tags(self, queryset, tags, value):
        tags = Tag.objects.get(name__icontains=value)
        filtered_posts = queryset.filter(tags=tags)
        return filtered_posts


class ProfileFilter(FilterSet):
    nickname = filters.CharFilter(field_name='nickname', lookup_expr='icontains')
    follower = filters.CharFilter(method='filter_by_following')

    class Meta:
        model = Profile
        fields = ['nickname']

    def filter_by_following(self, queryset, following, value):
        following = Follow.objects.get(following__nickname__iexact=value)
        filtered_users = queryset.filter(following=following)
        return filtered_users
