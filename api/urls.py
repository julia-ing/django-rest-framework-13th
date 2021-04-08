from django.urls import path
from api import views

urlpatterns = [
    path('posts/', views.PostList.as_view(), name='posts'),
    path('posts/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('users/', views.ProfileList.as_view(), name='users'),
    path('users/<int:pk>', views.ProfileDetail.as_view(), name='user_detail')
]
