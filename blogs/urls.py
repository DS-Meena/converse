from . import views
from django.urls import path

from .views import add_post
from blogs.views import blog_list_view

app_name = 'blogs'

urlpatterns = [
    path('', views.PostList.as_view(), name="blogs"),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('add_post/', add_post, name='add_post'),
    path('<slug:slug>/', views.post_detail, name="post_detail"),
    path('list/<user_id>/', blog_list_view, name='list'),
    path('update_status/<str:slug>/',views.updateStatus,name='update_status'),
]