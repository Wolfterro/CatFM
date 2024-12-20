from django.urls import path
from apps.radio.consumers import AudioStreamConsumer

websocket_urlpatterns = [
    path('ws/audio_stream/<int:room_id>/', AudioStreamConsumer.as_asgi()),
]