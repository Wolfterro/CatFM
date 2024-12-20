import os
import hashlib
from django.core.management.base import BaseCommand, CommandError

from apps.streaming.models import Audio


class Command(BaseCommand):
    help = 'Aceita um caminho de pasta como argumento e o imprime.'

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            type=str,
            help='O caminho da pasta a ser exibido.',
        )

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        if not os.path.isdir(path):
            raise CommandError(f'O caminho fornecido "{path}" não é um diretório válido.')

        mp3_files = self.get_mp3_files(path)
        self.register_mp3_files(mp3_files)

    # Auxiliary Methods
    # -----------------
    def get_mp3_files(self, path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]

    def register_mp3_files(self, mp3_files):
        for mp3_file in mp3_files:
            filename = os.path.basename(mp3_file).replace(".mp3", "")
            md5 = hashlib.md5(open(mp3_file, 'rb').read()).hexdigest()
            if Audio.objects.filter(md5=md5).exists():
                self.stdout.write(self.style.WARNING(f'Arquivo "{filename}" duplicado! Pulando...'))
                continue

            with open(mp3_file, 'rb') as audio_file:
                audio = Audio()
                audio.name = filename
                audio.format = 'mp3'
                audio.album = 'Added by Sniffer'
                audio.artist = 'Artista Desconhecido'
                audio.year = 0
                audio.is_active = False
                audio.file.save(filename, audio_file, save=True)
                audio.save()

            self.stdout.write(self.style.SUCCESS(f'Arquivo "{filename}" adicionado com sucesso!'))
