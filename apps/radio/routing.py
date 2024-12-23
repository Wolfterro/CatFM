from django.urls import path
from apps.radio.consumers import RadioStreamConsumer

websocket_urlpatterns = [
    path('ws/radio/<str:radiostream_identifier>/', RadioStreamConsumer.as_asgi()),
]