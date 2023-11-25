from django.urls import path, re_path
from . import views
from .tools import get_code_regex

urlpatterns = [
    path("play/<lobby_id>", views.lobby_page, name="play"),
    path("play/create/<module_id>", views.create_game, name="create"),
    path("host/", views.host_lobby_page, name="host"),
    path("play/", views.join_game, name="join"),
]