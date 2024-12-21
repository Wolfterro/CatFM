from django.contrib import admin

from apps.streaming.models import Audio, DownloadRequest

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


class DownloadRequestAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_download_request_change_form.html"

    list_display = ('url', 'status', 'approved_at')
    list_filter = ('status', 'approved_at')
    search_fields = ('url', 'status', 'approved_at')
    ordering = ('url', 'status', 'approved_at')

    class Meta:
        model = DownloadRequest


admin.site.register(DownloadRequest, DownloadRequestAdmin)
admin.site.register(Audio, AudioAdmin)