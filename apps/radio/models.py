import uuid

from django.db import models

# Create your models here.
# ========================
class Radio(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    description = models.TextField(default=None, blank=True, null=True)
    cover = models.FileField(upload_to='radio/cover/', default=None, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Properties
    @property
    def playing_now(self):
        return self.radio_streams.filter(is_active=True).first()


class RadioStream(models.Model):
    radio = models.ForeignKey(Radio, on_delete=models.SET_NULL, null=True, blank=True, related_name="radio_streams")
    audios = models.ManyToManyField('streaming.Audio', blank=True)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255, default=None, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[{}] {}".format(self.radio.name, self.title)

    # Properties
    @property
    def total_duration(self):
        return sum([audio.duration_in_seconds for audio in self.audios.all()])
