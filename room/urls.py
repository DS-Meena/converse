from django.urls import path

from room.views import (
	room,
)

app_name = 'room'

urlpatterns = [
    path('<str:room_name>/', room, name='room'),
]