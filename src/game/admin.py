from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Lobby, LobbySettings, LobbyPlayer


class LobbySettingsInline(admin.TabularInline):
    model = LobbySettings
    max_num = 1

class LobbyPlayersInline(admin.TabularInline):
    model = LobbyPlayer
    extra = 0


@admin.register(LobbyPlayer)
class LobbyPlayerAdmin(admin.ModelAdmin):
    list_display = ['player_id', 'name', 'lobby', 'points']

@admin.register(Lobby)
class LobbyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Lobby._meta.get_fields() if field.name not in ['id', 'secret', 'uuid', 'created_at', 'updated_at', "players"]]
    inlines = [LobbySettingsInline, LobbyPlayersInline]
    readonly_fields = ['code']

@admin.register(LobbySettings)
class LobbySettingsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LobbySettings._meta.get_fields()]
