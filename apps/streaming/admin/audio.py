from django.contrib import admin

from apps.streaming.models import Audio


class AudioAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_audio_change_form.html"

    filter_horizontal = ('genres', )

    list_display = ('name', 'album', 'artist', 'year', 'genres_list', 'identifier', 'is_active', 'created_at', 'updated_at')
    list_filter = ('album', 'artist', 'year')
    search_fields = ('name', 'album', 'artist', 'year', 'identifier')
    ordering = ('name', 'album', 'artist', 'year', 'created_at', 'updated_at')

    class Meta:
        model = Audio

admin.site.register(Audio, AudioAdmin)