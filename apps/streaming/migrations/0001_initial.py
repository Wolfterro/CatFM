# Generated by Django 4.2.17 on 2024-12-19 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('album', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('artist', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('year', models.IntegerField(default=0)),
                ('cover', models.FileField(upload_to='')),
                ('cover_url', models.URLField(blank=True, default=None, null=True)),
                ('file', models.FileField(upload_to='')),
                ('format', models.CharField(default='mp3', max_length=5)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
