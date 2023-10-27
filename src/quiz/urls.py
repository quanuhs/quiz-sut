from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.main_page),
    path("module/all", views.modules_page, name="modules"),
    path("module/<id>", views.module_page, name="module"),
    path("module/edit/<id>", views.module_page, name="edit_module"),
    path("author/<id>", views.author_page, name="author"),
    path("login", views.login_page, name="login")
]