from django.contrib import admin

from apps.streaming.services.downloader import Downloader


@admin.action(description="Aprovar requisições selecionadas")
def approve_requests(modeladmin, request, queryset):
    downloader = Downloader(queryset)
    downloader.download()

@admin.action(description="Recusar requisições selecionadas")
def reject_requests(modeladmin, request, queryset):
    queryset.update(status="rejected")
