from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(f'ws/socket-server/', consumers.GameConsumer.as_asgi())
]