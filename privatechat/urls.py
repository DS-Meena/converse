from django.urls import path

from privatechat.views import(
	private_chat_room_view,
)

app_name = 'privatechat'

urlpatterns = [
	path('', private_chat_room_view, name='private-chat-room'),
]