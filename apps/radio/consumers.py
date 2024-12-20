from channels.generic.websocket import AsyncWebsocketConsumer


class AudioStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"audio_stream_{self.room_id}"

        # Adiciona o usuário ao grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove o usuário do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Reenvia os dados de áudio recebidos para o grupo
        if bytes_data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'audio_message',
                    'bytes_data': bytes_data
                }
            )

    async def audio_message(self, event):
        # Envia os dados de áudio para o WebSocket
        bytes_data = event['bytes_data']
        await self.send(bytes_data=bytes_data)
