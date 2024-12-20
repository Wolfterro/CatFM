import threading
import subprocess


class HLSConverterService(object):
    def __init__(self, audio, identifier):
        self.audio = audio

    def convert_to_hls(self):
        threading.Thread(target=self._thread_convert_to_hls).start()

    # "Private" Methods
    # -----------------
    def _thread_convert_to_hls(self):
        output_playlist = "{}/{}".format(self.audio.folder, f"{self.audio.name.split('.')[0]}.m3u8")
        command = [
            "ffmpeg", "-i", self.audio.file.path,
            "-codec:a", "aac", "-b:a", "128k",
            "-hls_time", "10", "-hls_list_size", "0",
            "-hls_segment_filename", "{}/{}".format(self.audio.folder, f"{self.audio.name.split('.')[0]}_%03d.aac"),
            str(output_playlist)
        ]
        subprocess.run(command, check=True)
