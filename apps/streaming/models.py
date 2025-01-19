import os
import uuid
import hashlib
import threading
from urllib.parse import urlparse, parse_qs

from django.db import models
from django.utils import timezone
from django.conf import settings

from apps.streaming.utils import upload_to_instance_folder
from apps.streaming.services.hls_converter import HLSConverterService
from apps.streaming.services.downloader import Downloader


# Create your models here.
# ========================
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nome')

    def __str__(self):
        return self.name

    @staticmethod
    def populate():
        genres_list = [
            "Rock",
            "Pop",
            "Hip Hop",
            "Rap",
            "R&B",
            "Jazz",
            "Blues",
            "Gospel",
            "Reggae",
            "Funk",
            "Sertanejo",
            "Forró",
            "MPB",
            "Bossa Nova",
            "Samba",
            "Pagode",
            "Country",
            "Folk",
            "Eletrônica",
            "House",
            "Techno",
            "Trance",
            "Phonk",
            "Vaporwave",
            "Synthwave",
            "Dubstep",
            "Drum and Bass",
            "Trap",
            "K-Pop",
            "J-Pop",
            "Cumbia",
            "Bachata",
            "Reggaeton",
            "Merengue",
            "Salsa",
            "Bolero",
            "Heavy Metal",
            "Hard Rock",
            "Punk",
            "Emo",
            "Grunge",
            "Indie",
            "Alternative Rock",
            "Progressive Rock",
            "Classic Rock",
            "New Age",
            "World Music",
            "Afrobeat",
            "Kizomba",
            "Zouk",
            "Opera",
            "Classical",
            "Baroque",
            "Chillout",
            "Lo-fi",
            "Ambient",
            "Experimental",
            "Industrial",
            "Soundtrack",
            "Musical",
            "Choro",
            "Axé",
            "Tango",
            "Polka",
            "Hardcore",
            "Death Metal",
            "Black Metal",
            "Thrash Metal",
            "Gothic",
            "Post-Rock",
            "Shoegaze",
            "Dream Pop",
            "Dub",
            "Dancehall",
            "Future Bass",
            "Moombahton",
            "Electro",
            "Chiptune",
            "Jungle",
            "Garage",
            "Breakbeat",
            "Ska",
            "Math Rock",
            "Post-Hardcore",
            "Screamo",
            "Art Rock",
            "Drone",
            "Avant-Garde",
            "Ethnic",
            "Latin",
            "Turkish",
            "Arabic",
            "Bollywood",
            "Carnatic",
            "Hindustani",
            "Flamenco"
        ]
        for genre in genres_list:
            Genre.objects.get_or_create(name=genre)


class Audio(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Identificador')

    name = models.CharField(max_length=255, verbose_name='Nome')
    album = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name='Álbum')
    artist = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name='Artista')
    year = models.IntegerField(default=0, verbose_name='Ano')
    duration_in_seconds = models.IntegerField(default=0, verbose_name='Duração (em segundos)')
    cover = models.FileField(upload_to=upload_to_instance_folder, default=None, blank=True, null=True, verbose_name='Capa')
    cover_url = models.URLField(default=None, blank=True, null=True, verbose_name='URL da capa')

    genres = models.ManyToManyField(Genre, blank=True, verbose_name='Gêneros')

    file = models.FileField(upload_to=upload_to_instance_folder, verbose_name='Arquivo')
    format = models.CharField(max_length=5, default="mp3", verbose_name='Formato')
    md5 = models.CharField(max_length=32, default=None, editable=False, verbose_name='MD5')

    is_active = models.BooleanField(default=True, verbose_name='Ativo?')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return "{} - {} ({})".format(self.artist, self.name, self.year)

    def save(self, *args, **kwargs):
        old_file = self.file
        if not self.id:
            self.md5 = hashlib.md5(open(self.file.path, 'rb').read()).hexdigest()
            super(Audio, self).save(*args, **kwargs)

        if not self.duration_in_seconds or (self.file and old_file != self.file):
            if self.format == "mp3":
                from mutagen.mp3 import EasyMP3
                audio = EasyMP3(self.file.path)
                self.duration_in_seconds = audio.info.length

        super(Audio, self).save(*args, **kwargs)
        hls_converter = HLSConverterService(self, self.identifier)
        hls_converter.convert_to_hls()

    # Properties
    @property
    def folder(self):
        return self.file.path.replace(self.file.name, str(self.identifier))

    @property
    def cover_full_url(self):
        return self.cover.url if self.cover else self.cover_url

    @property
    def file_stream_m3u8_url(self):
        files = os.listdir(self.folder)
        for f in files:
            if f.endswith(".m3u8"):
                return "{}{}/{}".format(settings.MEDIA_URL, self.identifier, f)

    @property
    def genres_list(self):
        return [g.name for g in self.genres.all()]
    genres_list.fget.short_description = "Gêneros"

    @property
    def file_url(self):
        url = self.file.url if self.file else None
        if not url:
            return None

        return url


class DownloadRequest(models.Model):
    audio = models.ForeignKey(Audio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Áudio")
    url = models.URLField(verbose_name="URL")
    title = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name="Título")
    requested_by = models.ForeignKey("catuser.CatUser", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Solicitado por")

    status = models.CharField(max_length=255, default="pending", choices=[
        ("pending", "Pendente"),
        ("approved", "Aprovado"),
        ("rejected", "Rejeitado")
    ], verbose_name="Status")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Aprovado em")

    def __str__(self):
        return "[{}] {}".format(self.get_status_display(), self.url)

    # Properties
    @property
    def url_id(self):
        parsed_url = urlparse(self.url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]

    # Auxiliary Methods
    # -----------------
    def register(self, file_info):
        try:
            file = open(file_info.get('path'), "rb")

            audio = Audio()
            audio.name = file_info.get('name')
            audio.format = file_info.get('format')
            audio.album = file_info.get('album')
            audio.artist = file_info.get('artist')
            audio.year = file_info.get('year')
            audio.cover_url = file_info.get('cover_url')
            audio.file.save("{}.{}".format(file_info.get('name'), file_info.get('format')), file, save=True)
            audio.save()
        except Exception as e:
            print(">>> Erro ao registrar: {}".format(e))
            return None

        self.status = "approved"
        self.approved_at = timezone.now()
        self.audio = audio
        self.save()

        added_recently_playlist = Playlist.objects.filter(
            name__iexact="Adicionados Recentemente",
            is_system_playlist=True
        ).first()
        if added_recently_playlist:
            added_recently_playlist.audios.add(audio)
            added_recently_playlist.save()

    def set_info(self):
        downloader = Downloader([self])
        info_list = downloader.get_info()

        try:
            info = info_list[0]
            self.title = info.get('title')
            self.save()
        except Exception as e:
            print(">>> Erro ao registrar: {}".format(e))
            return None

        return info


class AdminRequest(models.Model):
    link_list = models.TextField(default=None, blank=True, null=True, verbose_name="Lista de links")
    link_list_file = models.FileField(upload_to='admin_requests/', default=None, blank=True, null=True, verbose_name="Arquivo com a lista de links")

    status = models.CharField(max_length=255, default="pending", choices=[
        ("pending", "Pendente"),
        ("done", "Finalizado"),
        ("error", "Erro"),
        ("in_process", "Em Processo")
    ], verbose_name="Status")
    link_status_description = models.TextField(default=None, blank=True, null=True, verbose_name="Descrição de status dos links")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return "[{}] Requisição criada em: {}".format(
            self.get_status_display(),
            timezone.localtime(self.created_at).strftime("%d/%m/%Y %H:%M:%S")
        )

    def save(self, *args, **kwargs):
        from apps.streaming.services.admin_request_downloader import AdminRequestDownloaderService

        download_service = AdminRequestDownloaderService(self)
        threading.Thread(target=download_service.download_links).start()

        self.status = "in_process"
        super(AdminRequest, self).save(*args, **kwargs)

    # Properties
    @property
    def link_list_array(self):
        if self.link_list_file:
            content = self.link_list_file.file.read().decode('utf-8').replace("\r", "").split("\n")
            return [x for x in content if x not in ['', None]]

        return self.link_list.split("\r\n")


class Playlist(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Identificador")

    can_be_shared = models.BooleanField(default=True, verbose_name="Pode ser compartilhada?")
    audios = models.ManyToManyField(Audio, blank=True, verbose_name="Áudios")
    owner = models.ForeignKey("catuser.CatUser", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")

    is_system_playlist = models.BooleanField(default=False, verbose_name="É playlist de sistema?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return "[{}] {}{}".format(
            "Pública" if self.can_be_shared else "Privada",
            self.name,
            " (Sistema)" if self.is_system_playlist else " ({})".format(self.owner if self.owner else "Usuário excluído")
        )

    def save(self, *args, **kwargs):
        if self.is_system_playlist:
            self.owner = None
            self.can_be_shared = True

        super(Playlist, self).save(*args, **kwargs)

    # Properties
    @property
    def cover(self):
        if not self.audios.exists():
            return None

        audio = self.audios.first()
        return audio.cover_url if audio.cover_url else (audio.cover.url if audio.cover else None)
