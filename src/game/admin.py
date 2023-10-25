from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Lobby, LobbySettings


class LobbySettingsInline(admin.TabularInline):
    model = LobbySettings
    max_num = 1

@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Lobby._meta.get_fields()]
    inlines = [LobbySettingsInline]

@admin.register(LobbySettings)
class LobbySettingsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LobbySettings._meta.get_fields()]
