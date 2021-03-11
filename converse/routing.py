from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path

# trying using converse.routing file without asgi
from room.consumers import ChatConsumer

application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter([
					path('room/<room_name>/', ChatConsumer),
			])
		)
	),
})