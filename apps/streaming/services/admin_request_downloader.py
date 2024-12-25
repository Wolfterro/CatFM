import os

import yt_dlp

from django.conf import settings
from django.utils import timezone

from apps.streaming.models import Audio, Playlist, AdminRequest


class AdminRequestDownloaderService(object):
    def __init__(self, admin_request):
        self.admin_request = admin_request

    def download_links(self):
        link_list = self.admin_request.link_list_array
        download_status = []

        for link in link_list:
            download_status.append(
                dict(
                    url=link,
                    status="in_progress",
                    error=None,
                    info_dict=None
                )
            )

        try:
            self._download_links(download_status)
            self._assemble_status_description(download_status)
        except Exception as e:
            print(">>> Erro ao baixar: {}".format(e))
            self.admin_request.status = "error"
            self.admin_request.link_status_description = ">>> Erro ao baixar: {}\n".format(e)
            super(AdminRequest, self.admin_request).save()

    # Auxiliary Methods
    # -----------------
    def _download_links(self, download_status):
        for download in download_status:
            info = self._get_info(download)
            if download['status'] == "error":
                continue

            self._download_and_register(download, info)
            if download['status'] == "error":
                continue

            download['status'] = 'done'

    def _get_info(self, download):
        try:
            ytdl_opts = {}
            with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                info = ydl.extract_info(download['url'], download=False)

            return info
        except Exception as e:
            print(">>> Erro ao baixar: {}".format(download['url']))
            download['error'] = str(e)
            download['status'] = "error"
            return None

    def _download_and_register(self, download, info):
        info_dict = {
            'name': info.get('title'),
            'path': "{}/{}.{}".format(settings.DOWNLOAD_PATH, info.get('title'), "mp3"),
            'format': "mp3",
            'album': info.get('album', 'Album Desconhecido'),
            'artist': info.get('artists', ['Artista Desconhecido'])[0],
            'year': info.get('release_year', 0) or 0,
            'cover_url': info.get('thumbnail', None)
        }
        download['info_dict'] = info_dict

        ytdl_opts = {
            'format': 'mp3/bestaudio/best',
            'outtmpl': "{}/{}".format(settings.DOWNLOAD_PATH, info_dict.get('name')),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
            error_code = ydl.download(download['url'])

        if error_code:
            print(">>> Erro ao baixar: {}".format(download['url']))
            download['status'] = "error"
            download['error'] = error_code

        print(">>> Audio baixado: {}! Registrando...".format(download['url']))
        self._register(download, info_dict)
        self._clean_download_file(info_dict)

    def _register(self, download, file_info):
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
            download['status'] = "error"
            download['error'] = str(e)
            return None

        added_recently_playlist = Playlist.objects.filter(
            name__iexact="Adicionados Recentemente",
            is_system_playlist=True
        ).first()
        if added_recently_playlist:
            added_recently_playlist.audios.add(audio)
            added_recently_playlist.save()

    def _clean_download_file(self, info):
        os.remove(info.get('path'))

    def _assemble_status_description(self, download_status):
        description = ""
        for download in download_status:
            info = download['info_dict']
            if info:
                description += ">>>>>> Audio: {} - {} ({})!\n".format(
                    info['artist'],
                    info['name'],
                    info['year']
                )

            if Audio.objects.filter(
                name=download['info_dict']['name'],
                created_at__date__lt=timezone.now().date()
            ).exists():
                description += ">>> Audio já registrado!\n"

            if download['status'] == "error":
                description += ">>> Erro ao baixar: {}\n".format(download['error'])
                self.admin_request.status = "error"
            elif download['status'] == "done":
                description += ">>> Audio baixado!\n\n"
                self.admin_request.status = "done"
            else:
                description += ">>> Baixando...!\n\n"
                self.admin_request.status = "in_process"

        self.admin_request.link_status_description = description
        super(AdminRequest, self.admin_request).save()
