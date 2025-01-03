# Generated by Django 4.2.17 on 2024-12-30 02:03

import apps.streaming.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('streaming', '0015_genre_audio_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='adminrequest',
            name='link_list',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Lista de links'),
        ),
        migrations.AlterField(
            model_name='adminrequest',
            name='link_list_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='admin_requests/', verbose_name='Arquivo com a lista de links'),
        ),
        migrations.AlterField(
            model_name='adminrequest',
            name='link_status_description',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Descrição de status dos links'),
        ),
        migrations.AlterField(
            model_name='adminrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendente'), ('done', 'Finalizado'), ('error', 'Erro'), ('in_process', 'Em Processo')], default='pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='adminrequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='album',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Álbum'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='artist',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Artista'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='cover',
            field=models.FileField(blank=True, default=None, null=True, upload_to=apps.streaming.utils.upload_to_instance_folder, verbose_name='Capa'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='cover_url',
            field=models.URLField(blank=True, default=None, null=True, verbose_name='URL da capa'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='duration_in_seconds',
            field=models.IntegerField(default=0, verbose_name='Duração (em segundos)'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='file',
            field=models.FileField(upload_to=apps.streaming.utils.upload_to_instance_folder, verbose_name='Arquivo'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='format',
            field=models.CharField(default='mp3', max_length=5, verbose_name='Formato'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='genres',
            field=models.ManyToManyField(blank=True, to='streaming.genre', verbose_name='Gêneros'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Identificador'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Ativo?'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='md5',
            field=models.CharField(default=None, editable=False, max_length=32, verbose_name='MD5'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='year',
            field=models.IntegerField(default=0, verbose_name='Ano'),
        ),
        migrations.AlterField(
            model_name='downloadrequest',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Aprovado em'),
        ),
        migrations.AlterField(
            model_name='downloadrequest',
            name='audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='streaming.audio', verbose_name='Áudio'),
        ),
        migrations.AlterField(
            model_name='downloadrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='downloadrequest',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Solicitado por'),
        ),
        migrations.AlterField(
            model_name='downloadrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendente'), ('approved', 'Aprovado'), ('rejected', 'Rejeitado')], default='pending', max_length=255, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='downloadrequest',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='downloadrequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='downloadrequest',
            name='url',
            field=models.URLField(verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='audios',
            field=models.ManyToManyField(blank=True, to='streaming.audio', verbose_name='Áudios'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='can_be_shared',
            field=models.BooleanField(default=True, verbose_name='Pode ser compartilhada?'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Identificador'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='is_system_playlist',
            field=models.BooleanField(default=False, verbose_name='É playlist de sistema?'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
    ]
