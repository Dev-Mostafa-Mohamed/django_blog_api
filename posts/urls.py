from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.api_login),
    path('api/posts/',views.api_post_list,name="api_post_list"),
    path('api/create/',views.api_create_post,name="api_create_post"),
    path('api/posts/<int:pk>/', views.api_post_detail,name="api_post_detail"),
]