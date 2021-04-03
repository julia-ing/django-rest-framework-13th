from django.urls import path
from api import views

urlpatterns = [
    path('posts/', views.post_list),
    path('posts/<int:pk>', views.get_one_post)
]
