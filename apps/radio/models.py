import uuid

from django.db import models

# Create your models here.
# ========================
class Radio(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Identificador")

    description = models.TextField(default=None, blank=True, null=True, verbose_name="Descrição")
    cover = models.FileField(upload_to='radio/cover/', default=None, blank=True, null=True, verbose_name="Capa")

    is_active = models.BooleanField(default=True, verbose_name="Ativo?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return self.name

    # Properties
    @property
    def playing_now(self):
        return self.radio_streams.filter(is_active=True).first()


class RadioStream(models.Model):
    radio = models.ForeignKey(Radio, on_delete=models.SET_NULL, null=True, blank=True, related_name="radio_streams", verbose_name="Rádio")
    audios = models.ManyToManyField('streaming.Audio', blank=True, verbose_name="Audios")
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Identificador")

    title = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name="Título")

    is_active = models.BooleanField(default=False, verbose_name="Ativo?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return "[{}] {}".format(self.radio.name, self.title)

    # Properties
    @property
    def total_duration(self):
        return sum([audio.duration_in_seconds for audio in self.audios.all()])
