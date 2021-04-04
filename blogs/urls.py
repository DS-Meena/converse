from . import views
from django.urls import path

from .views import add_post


urlpatterns = [
    path('blogs/', views.PostList.as_view()),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('blogs/add_post', add_post, name='add_post')
]