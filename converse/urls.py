"""converse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# get urls from other apps (account)
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path

# for the static, media files
from django.conf.urls.static import static

# for account verification (password reset)
from django.contrib.auth import views as auth_views


# import the views from chatapp
from chatapp.views import (
	home_screen_view
)

# import the views from account (app)
from account.views import (
    # related to user management
    register_view,
    login_view,
    logout_view,
    account_search_view,
)


# import the views from chatroom(app)
# from chatroom.views import (
#     # related to the public chatrooms
#     my_chatroom,
# )

# for second one
from room.views import (
    # realted to public chatrooms
    room,
) 

urlpatterns = [
	# add the main page view of chatapp
	path('', home_screen_view, name='home'),
    path('admin/', admin.site.urls),

    # link to the user account pages (inside app)
    path('account/', include('account.urls', namespace='account')),

    # link to the friend system
    path('friends/', include('friends.urls', namespace='friend')),

    # add link for the user registration
    path('register/', register_view, name="register"),

    # link to the login and logout pages
    path('login/', login_view, name="login"), 
    path('logout/', logout_view, name="logout"),

    # link to the result of searach (header)
    path('search/', account_search_view, name="search"), 

    # link to the chatrooms pages (inside app)
    # path('chatroom/', include('chatroom.urls', namespace='chatroom')),

    # link to the chatroom pages (inside app) (second one)
    path('room/', include('room.urls', namespace='room')),

    #link to blogs
    path('blogs/', include('blogs.urls',)),

    # link to the quick chat room
    path('quickchat/', include('quickchat.urls', namespace='quickchat')),

    # link to private chat links
    path('privatechat/', include('privatechat.urls', namespace='privatechat')),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    # templates added manually
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
]

# for the static, meida files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
