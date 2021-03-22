import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.core.asgi import get_asgi_application

import room.routing
import quickchat.routing

from room.consumers import ChatConsumer
from quickchat.consumers import ChatConsumer as CC

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "converse.settings")


# asgi application for routing of web sockets
application = ProtocolTypeRouter({
  # to handle traditional http request
    "http": get_asgi_application(),

    # web socket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r'ws/room/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
            url(r'ws/quickchat/(?P<room_name>\w+)/(?P<user_handle>\w+)/$', CC.as_asgi()),
          ]

            # room.routing.websocket_urlpatterns,
            # does not with different routing
            # quickchat.routing.websocket_urlpatterns
        )
    ),
})