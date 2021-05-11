from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework import routers
from .views import PostViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)   # register()함으로써 두 개의 url 생성
router.register(r'users', ProfileViewSet)

urlpatterns = router.urls

#  CBV
# urlpatterns = [
#     path('posts/', views.PostList.as_view(), name='posts'),
#     path('posts/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
#     path('users/', views.ProfileList.as_view(), name='users'),
#     path('users/<int:pk>', views.ProfileDetail.as_view(), name='user_detail')
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)


