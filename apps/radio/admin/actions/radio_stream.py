import threading

from django.contrib import admin
from django.contrib import messages

from apps.radio.services.broadcast import BroadcastService


@admin.action(description="Iniciar/Reiniciar transmissões selecionadas")
def start_broadcasts(modeladmin, request, queryset):
    count = queryset.count()

    for radio_stream in queryset:
        broadcast_service = BroadcastService(radio_stream.identifier)
        threading.Thread(target=broadcast_service.start_broadcast).start()

    message = "Sucesso! Aguarde enquanto a automação faz a inicialização das {} transmissões em segundo plano.".format(count)
    modeladmin.message_user(
        request,
        message,
        level=messages.SUCCESS
    )


@admin.action(description="Desativar transmissões selecionadas")
def stop_broadcasts(modeladmin, request, queryset):
    count = queryset.count()

    for radio_stream in queryset:
        broadcast_service = BroadcastService(radio_stream.identifier)
        threading.Thread(target=broadcast_service.stop_broadcast).start()

    message = "Sucesso! Aguarde enquanto a automação faz a desativação das {} transmissões em segundo plano.".format(count)
    modeladmin.message_user(
        request,
        message,
        level=messages.SUCCESS
    )
