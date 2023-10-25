from django.urls import re_path, path
from . import consumers
from .tools import get_code_regex, get_uuid_regex

websocket_urlpatterns = [
    path(f'game/player/<str:lobby_id>/', consumers.GamePlayerConsumer.as_asgi()),
    path(f'game/admin/<str:secret_id>/', consumers.GameAdminConsumer.as_asgi())
]