import uuid
import hashlib
from django.db import models

from apps.streaming.utils import upload_to_instance_folder
from apps.streaming.services.hls_converter import HLSConverterService


# Create your models here.
# ========================
class Audio(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    album = models.CharField(max_length=255, default=None, blank=True, null=True)
    artist = models.CharField(max_length=255, default=None, blank=True, null=True)
    year = models.IntegerField(default=0)
    duration_in_seconds = models.IntegerField(default=0)
    cover = models.FileField(upload_to=upload_to_instance_folder, default=None, blank=True, null=True)
    cover_url = models.URLField(default=None, blank=True, null=True)

    file = models.FileField(upload_to=upload_to_instance_folder)
    format = models.CharField(max_length=5, default="mp3")
    md5 = models.CharField(max_length=32, default=None, editable=False)

    is_active = models.BooleanField(default=True)

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
