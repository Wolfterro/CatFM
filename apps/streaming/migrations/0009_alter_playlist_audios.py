# Generated by Django 4.2.17 on 2024-12-21 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0008_playlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='audios',
            field=models.ManyToManyField(blank=True, to='streaming.audio'),
        ),
    ]