from django.urls import path, re_path
from . import views
from .tools import get_code_regex

urlpatterns = [
    re_path(f'play/{get_code_regex()}', views.test)
]