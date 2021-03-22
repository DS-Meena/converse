from django.urls import path

from chatroom.views import (
	my_chatroom,
)

app_name = 'chatroom'

urlpatterns = [
    path('<str:room_name>/', my_chatroom, name='my_chatroom'),
]