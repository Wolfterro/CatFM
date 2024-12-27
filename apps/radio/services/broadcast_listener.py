import os
import json
import uuid
import psutil
import websockets
from asgiref.sync import async_to_sync

from django.conf import settings

from apps.radio.models import RadioStream


class BroacastListenerService(object):
    def get_active_broadcasts(self):
        active_pids = self.__get_active_pids()
        detailed_info = self.__get_process_detailed_info(active_pids)
        return detailed_info

    # Auxiliary Methods
    # -----------------
    def __get_active_pids(self):
        path = "{}/logs".format(settings.BASE_DIR)
        pid_list = [f for f in os.listdir(path) if f.endswith('.pid')]
        active_pids = []

        for pid in pid_list:
            with open("{}/{}".format(path, pid), 'r') as pid_file:
                pid_int = int(pid_file.read())

                try:
                    process = psutil.Process(pid_int)
                    if process.is_running() and process.status() != psutil.STATUS_ZOMBIE:
                        details = {
                            "pid": process.pid,
                            "name": process.name(),
                            "executable_path": process.exe(),
                            "cmdline": " ".join(process.cmdline()),
                            "cmdline_raw": process.cmdline(),
                            "status": process.status(),
                            "username": process.username(),
                            "create_time": process.create_time(),
                            "cpu_percent": process.cpu_percent(interval=1.0),
                            "mem_usage": process.memory_info().rss,
                            "num_threads": process.num_threads()
                        }
                        active_pids.append(details)
                except Exception:
                    continue

        return active_pids

    def __get_process_detailed_info(self, active_pids):
        for pid in active_pids:
            cmdline_raw = pid.get('cmdline_raw')
            for i in cmdline_raw:
                if not self.__is_valid_uuid4(i):
                    continue

                radio_stream = RadioStream.objects.filter(identifier=i).first()
                if radio_stream:
                    pid['radio_stream'] = dict(
                        identifier=radio_stream.identifier,
                        title=radio_stream.title,
                        radio=radio_stream.radio.name,
                        playing_now=async_to_sync(self.__probe_broadcast_information)(radio_stream.identifier)
                    )

        return active_pids

    def __is_valid_uuid4(self, string):
        try:
            uuid.UUID(string, version=4)
            return True
        except ValueError:
            return False

    async def __probe_broadcast_information(self, radiostream_identifier):
        uri = f"ws://localhost:8000/ws/radio/{radiostream_identifier}/"

        async with websockets.connect(uri) as websocket:
            counter = 0
            while True:
                if counter > 10:
                    break

                message = await websocket.recv()
                message_json = json.loads(message) if message else None
                if message_json and "audio_name" in message_json:
                    return message_json

                counter += 1

        return None
