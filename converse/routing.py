from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path

from privatechat.consumers import ChatConsumer
from room.consumers import PublicChatConsumer

application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter([
					path('privatechat/<room_id>/', ChatConsumer),
					path('room/<room_name>/', PublicChatConsumer),
			])
		)
	),
})