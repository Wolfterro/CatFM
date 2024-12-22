import threading
from django.contrib import admin
from django.contrib import messages

from apps.streaming.services.downloader import Downloader


@admin.action(description="Aprovar requisições selecionadas")
def approve_requests(modeladmin, request, queryset):
    count = queryset.count()
    threading.Thread(target=Downloader(queryset).download).start()

    message = "Sucesso! Aguarde enquanto a automação faz o download das {} requisições em segundo plano.".format(count)
    modeladmin.message_user(
        request,
        message,
        level=messages.SUCCESS
    )

@admin.action(description="Recusar requisições selecionadas")
def reject_requests(modeladmin, request, queryset):
    queryset.update(status="rejected")
