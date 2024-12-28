import os
import time
import json
import uuid
import subprocess

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.conf import settings

from apps.radio.models import RadioStream


class BroadcastService(object):
    def __init__(self, radio_stream_identifier):
        self.radio_stream_identifier = radio_stream_identifier
        self.radio_stream = RadioStream.objects.get(identifier=self.radio_stream_identifier)
        self.radio = self.radio_stream.radio

    def manage_broadcast(self):
        # Checar se outra transmissão não está rolando. Se estiver, mata.
        self.kill_current_broadcast()
        self.start_new_broadcast()

        # Inicia a transmissão
        while True:
            for audio in self.radio_stream.audios.all():
                transmission_identifier = uuid.uuid4()
                seconds_passed = 0
                self.broadcast_audio_information(audio, seconds_passed, transmission_identifier)

                while True:
                    if seconds_passed >= audio.duration_in_seconds:
                        break

                    time.sleep(1)
                    seconds_passed += 1
                    self.broadcast_audio_information(audio, seconds_passed, transmission_identifier)

            break # debugging - para parar a transmissão

    def start_broadcast(self):
        subprocess.run([
            'python',
            'manage.py',
            'start_broadcast',
            '--radiostream',
            str(self.radio_stream_identifier)
        ])

    def stop_broadcast(self):
        self.kill_current_broadcast()

    # Auxiliary Methods
    # -----------------
    def kill_current_broadcast(self):
        try:
            filename = "{}/{}".format(settings.LOGS_PATH, "radio_broadcast_{}.pid".format(self.radio.identifier))
            with open(filename, 'r+') as pid_file:
                os.kill(int(pid_file.read()), 9)
        except:
            # Pid não existe. Deixa que ele cria ao iniciar a transmissão
            pass

        RadioStream.objects.filter(radio=self.radio_stream.radio).update(is_active=False)

    def start_new_broadcast(self):
        self.pid = os.getpid()
        filename = "{}/{}".format(settings.LOGS_PATH, "radio_broadcast_{}.pid".format(self.radio.identifier))
        with open(filename, 'w+') as pid_file:
            pid_file.write(str(self.pid))

        self.radio_stream.is_active = True
        self.radio_stream.save(update_fields=['is_active'])

    def broadcast_audio_information(self, audio, seconds_passed, transmission_identifier):
        # Responsável por enviar informações da musica ao front-end via WebSocket
        # Necessário enviar segundos passados, para iniciar exatamente no ponto de reprodução.
        filename = "{}/{}".format(settings.LOGS_PATH, "broadcast_log_{}.log".format(self.radio.identifier))
        with open(filename, 'a+') as broadcast_log:
            broadcast_log.write(f'{self.pid} - {audio.identifier} - {audio.name} - {seconds_passed}\n')

        info_dict = {
            'pid': self.pid,
            'auth': settings.WEBSOCKETS_AUTH_KEY,
            'audio_identifier': str(audio.identifier),
            'audio_name': audio.name,
            'audio_artist': audio.artist,
            'audio_album': audio.album,
            'audio_year': audio.year,
            'seconds_passed': seconds_passed,
            'duration': audio.duration_in_seconds,
            'file': audio.file.url,
            'md5': audio.md5,
            'file_stream': audio.file_stream_m3u8_url,
            'transmission_identifier': str(transmission_identifier)
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("radio_stream_{}".format(str(self.radio_stream_identifier)), {
            'type': 'file_stream_info',
            'info': json.dumps(info_dict)
        })
