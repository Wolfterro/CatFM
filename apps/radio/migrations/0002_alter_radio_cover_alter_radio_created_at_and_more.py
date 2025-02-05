# Generated by Django 4.2.17 on 2024-12-30 02:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0016_alter_adminrequest_created_at_and_more'),
        ('radio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radio',
            name='cover',
            field=models.FileField(blank=True, default=None, null=True, upload_to='radio/cover/', verbose_name='Capa'),
        ),
        migrations.AlterField(
            model_name='radio',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='radio',
            name='description',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='radio',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Identificador'),
        ),
        migrations.AlterField(
            model_name='radio',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Ativo?'),
        ),
        migrations.AlterField(
            model_name='radio',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='radio',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='radiostream',
            name='audios',
            field=models.ManyToManyField(blank=True, to='streaming.audio', verbose_name='Audios'),
        ),
        migrations.AlterField(
            model_name='radiostream',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='radiostream',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Identificador'),
        ),
        migrations.AlterField(
            model_name='radiostream',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Ativo?'),
        ),
        migrations.AlterField(
            model_name='radiostream',
            name='radio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='radio_streams', to='radio.radio', verbose_name='Rádio'),
        ),
        migrations.AlterField(
            model_name='radiostream',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='radiostream',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
    ]
