from django.core.management.base import BaseCommand

from apps.streaming.models import DownloadRequest
from apps.streaming.services.downloader import Downloader


class Command(BaseCommand):
    help = 'Aprova e faz o download de todas as solicitações de download pendentes.'

    def handle(self, *args, **kwargs):
        queryset = DownloadRequest.objects.filter(status="pending", audio__isnull=True)

        if queryset.count() == 0:
            self.stdout.write(self.style.SUCCESS('Nenhuma solicitação pendente encontrada! Saindo...'))
            return None

        self.stdout.write(self.style.SUCCESS(f'{queryset.count()} solicitações pendentes encontradas!'))
        downloader = Downloader(queryset)
        downloader.download()
