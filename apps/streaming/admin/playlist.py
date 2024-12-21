from django.contrib import admin

from apps.streaming.models import Playlist


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'can_be_shared', 'owner', 'is_system_playlist')
    list_filter = ('can_be_shared', 'owner', 'is_system_playlist')
    search_fields = ('name', 'identifier')
    ordering = ('name', 'identifier')

    class Meta:
        model = Playlist


admin.site.register(Playlist, PlaylistAdmin)