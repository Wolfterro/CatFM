import os
import sys

from django.core.management.base import BaseCommand
from django.conf import settings
from daemon import DaemonContext  # Opcional, para daemonizar o processo

from apps.radio.services.broadcast import BroadcastService


class Command(BaseCommand):
    help = 'Inicia a transmissão de rádio.'
    IS_DAEMON = True

    def add_arguments(self, parser):
        parser.add_argument(
            '--radiostream',
            type=str,
            help='O identificador da transmissão de rádio RadioStream.'
        )

    def handle(self, *args, **kwargs):

        self.stdout.write('Iniciando o daemon de transmissão...')
        if self.IS_DAEMON:
            with DaemonContext(stdout=sys.stdout, stderr=sys.stderr):
                self.run_daemon(*args, **kwargs)
        else:
            self.run_daemon(*args, **kwargs)

    def run_daemon(self, *args, **kwargs):
        broadcast_service = BroadcastService(kwargs['radiostream'])
        broadcast_service.manage_broadcast()

        self.stdout.write('Transmissão iniciada.')

    def save_pid_to_file(self):
        pid = os.getpid()
        with open("{}/{}".format(settings.LOGS_PATH, "radio_broadcast.pid"), 'w') as pid_file:
            pid_file.write(str(pid))
