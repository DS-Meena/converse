from . import views
from django.urls import path

from .views import add_post

# app_name = 'blogs'

urlpatterns = [
    path('all/', views.PostList.as_view()),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('all/add_post', add_post, name='add_post')
]