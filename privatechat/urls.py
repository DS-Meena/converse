from django.urls import path

from privatechat.views import(
	private_chat_room_view,
	create_or_return_private_chat,
)

app_name = 'privatechat'

urlpatterns = [
	# for private chat room
	# path('<str:room_id>/', privatechat, name='privatechat'),

	path('', private_chat_room_view, name='private-chat-room'),
	path('create_or_return_private_chat/', create_or_return_private_chat, name='create-or-return-private-chat'),
]