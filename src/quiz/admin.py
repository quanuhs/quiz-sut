from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Topic, Module, Card


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("pk", "email", "username", "first_name", "last_name")
    list_display_links = ("pk", "email", "username", "first_name", "last_name")
    search_fields = ("email", "username")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "author", "created_at", "updated_at")
    list_display_links = ("pk", "title", "author", "created_at", "updated_at")
    search_fields = ("title", "author__username", "description")
    list_filter = ("author__username", "created_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "author", "created_at", "updated_at")
    list_display_links = ("pk", "title", "author", "created_at", "updated_at")
    search_fields = ("title", "author__username", "description")
    list_filter = ("author__username", "created_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("pk", "front_text", "back_text", "module", "created_at", "updated_at")
    list_display_links = ("pk", "front_text", "back_text", "module", "created_at", "updated_at")
    search_fields = ("title", "module__title", "description")
    list_filter = ("module__title", "created_at")
