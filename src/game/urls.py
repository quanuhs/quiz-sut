from django.urls import path, re_path
from . import views
from .tools import get_code_regex

urlpatterns = [
    path("play/quiz/<lobby_id>", views.lobby_page, name="play"),
    path("play/quiz/create/<module_id>", views.create_game, name="create"),
    path("host/", views.host_lobby_page, name="host"),
    path("play/quiz/", views.join_game, name="join"),

    path("play/solo/quiz/<module_id>", views.solo_quiz, name="solo_quiz"),
    path("play/solo/match/<module_id>", views.solo_match, name="solo_match")
]