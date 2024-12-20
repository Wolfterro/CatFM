import websockets
import asyncio
import os
from django.utils import timezone

from django.core.management.base import BaseCommand

from apps.streaming.models import Audio

class Command(BaseCommand):
    def handle(self, *args, **options):
        audio_queue = [x for x in Audio.objects.filter(is_active=True)]
        asyncio.run(self.send_audio(1, audio_queue))

    async def send_audio(self, room_id, audio_queue):
        # uri = f"ws://localhost:8000/ws/audio_stream/{room_id}/"
        uri = f"ws://localhost:8000/ws/signaling/"

        for audio in audio_queue:
            file_path = audio.file.path

            async with websockets.connect(uri) as websocket:
                # Leia e envie blocos binários de tamanho 16 KB
                with open(file_path, "rb") as audio_file:
                    audio_file.seek(0, os.SEEK_END)
                    file_size = audio_file.tell()
                    audio_file.seek(0)
                    chunk_size = 16384

                    await self.show_audio_information(
                        dict(
                            filename=file_path,
                            filesize=file_size,
                            timestamp=timezone.now().strftime("%d/%m/%Y - %H:%M:%S"),
                        )
                    )

                    while chunk := audio_file.read(chunk_size):
                        await websocket.send(chunk)
                        await asyncio.sleep(0.01)

    async def show_audio_information(self, info):
        print(">>> Enviando: {}...".format(info.get("filename")))
        print("> Tamanho: {} bytes".format(info.get("filesize")))
        print("> Adicionado em: {}".format(info.get("timestamp")))
        print("-" * 40)
        print("")
