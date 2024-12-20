from django.contrib import admin

from apps.streaming.models import Audio

# Register your models here.
# ==========================
class AudioAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_audio_change_form.html"

    list_display = ('name', 'album', 'artist', 'year', 'identifier', 'is_active')
    list_filter = ('album', 'artist', 'year')
    search_fields = ('name', 'album', 'artist', 'year', 'identifier')
    ordering = ('name', 'album', 'artist', 'year')

    class Meta:
        model = Audio

admin.site.register(Audio, AudioAdmin)