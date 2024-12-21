import os
import yt_dlp

from django.conf import settings


class Downloader(object):
    def __init__(self, download_request_list):
        self.download_request_list = download_request_list

    def download(self):
        for download_request in self.download_request_list:
            self._download_and_register(download_request)

    # "Private" Methods
    # -----------------
    def _download_and_register(self, download_request):
        info = self._get_download_info(download_request)
        if not info:
            print(">>> Erro ao baixar: {}".format(download_request.url))
            return None

        info_dict = {
            'name': info.get('title'),
            'path': "{}/{}.{}".format(settings.DOWNLOAD_PATH, info.get('title'), "mp3"),
            'format': "mp3",
            'album': info.get('album', 'Album Desconhecido'),
            'artist': info.get('artists', ['Artista Desconhecido'])[0],
            'year': info.get('release_year', 0) or 0,
            'cover_url': info.get('thumbnail', None)
        }

        ytdl_opts = {
            'format': 'mp3/bestaudio/best',
            'outtmpl': "{}/{}".format(settings.DOWNLOAD_PATH, info_dict.get('name')),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
            error_code = ydl.download(download_request.url)

        if error_code:
            print(">>> Erro ao baixar: {}".format(download_request.url))
            return None

        print(">>> Audio baixado: {}! Registrando...".format(download_request.url))
        download_request.register(info_dict)
        self._clean_download_file(info_dict)

    def _get_download_info(self, download_request):
        ytdl_opts = {}
        with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
            info = ydl.extract_info(download_request.url, download=False)

        return info

    def _clean_download_file(self, info):
        os.remove(info.get('path'))
