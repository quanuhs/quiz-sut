from django.urls import re_path

from . import consumers
from .tools import get_code_regex

websocket_urlpatterns = [
    re_path(f'ws/socket-server/{get_code_regex()}', consumers.GameConsumer.as_asgi())
]