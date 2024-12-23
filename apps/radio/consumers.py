import json
from django.conf import settings

from channels.generic.websocket import AsyncWebsocketConsumer


class RadioStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.radiostream_id = self.scope['url_route']['kwargs']['radiostream_identifier']
        self.room_group_name = f"radio_stream_{self.radiostream_id}"

        # Adiciona o usuário ao grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'file_stream_info',
            'room_id': self.radiostream_id,
            'room_group_name': self.room_group_name
        }))

    async def disconnect(self, close_code):
        # Remove o usuário do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'file_stream_info',
                    'info': text_data
                }
            )

    async def audio_message(self, event):
        # Envia os dados de áudio para o WebSocket
        bytes_data = event['bytes_data']
        await self.send(bytes_data=bytes_data)


    async def file_stream_info(self, event):
        info = event['info']
        info_dict = json.loads(info)
        auth = info_dict.get('auth', None)

        if auth and auth == settings.WEBSOCKETS_AUTH_KEY:
            await self.send(text_data=info)
