from django.contrib import admin

from apps.streaming.models import DownloadRequest
from apps.streaming.admin.actions.download_request import approve_requests, reject_requests


class DownloadRequestAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_download_request_change_form.html"

    list_display = ('requested_by', 'title', 'url', 'status', 'approved_at')
    list_filter = ('status', 'approved_at')
    search_fields = ('url', 'status', 'approved_at')
    ordering = ('url', 'status', 'approved_at')
    actions = [approve_requests, reject_requests, ]

    class Meta:
        model = DownloadRequest

admin.site.register(DownloadRequest, DownloadRequestAdmin)
