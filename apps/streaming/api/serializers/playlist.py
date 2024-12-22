from apps.catuser.api.serializers import UserSerializer
from apps.streaming.api.serializers import StreamingSerializer
from apps.streaming.models import Playlist, Audio
from apps.catuser.models import CatUser

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PlaylistSerializer(serializers.ModelSerializer):
    audios = StreamingSerializer(many=True, read_only=True)
    audio_ids = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    owner = UserSerializer(read_only=True)
    owner_id = serializers.IntegerField(write_only=True)
    can_be_shared = serializers.BooleanField(read_only=True) # Disabling for now...
    is_system_playlist = serializers.BooleanField(read_only=True)

    class Meta:
        model = Playlist
        fields = [
            'name',
            'identifier',
            'owner',
            'owner_id',
            # 'can_be_shared', # Disabling for now...
            'is_system_playlist',
            'audios',
            'audio_ids',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        audios = validated_data.pop('audio_ids', [])
        owner_id = validated_data.pop('owner_id', None)
        if not owner_id:
            raise ValidationError({"detail": "Usuário inválido selecionado."})

        owner = CatUser.objects.filter(id=owner_id).first()
        if not owner:
            raise ValidationError({"detail": "Usuário inválido selecionado."})

        if owner != self.context['request'].user:
            raise ValidationError({"detail": "Não é possível criar uma playlist para outro usuário."})

        playlist = Playlist.objects.create(**validated_data)
        playlist.owner = owner

        for identifier in audios:
            audio = Audio.objects.get(identifier=identifier)
            playlist.audios.add(audio)

        playlist.save()
        return playlist

    def update(self, instance, validated_data):
        name = validated_data.pop('name', instance.name)
        can_be_shared = validated_data.pop('can_be_shared', instance.can_be_shared)
        audios = validated_data.pop('audio_ids', [])
        if len(audios) > 0:
            instance.audios.clear()

        for identifier in audios:
            audio = Audio.objects.get(identifier=identifier)
            instance.audios.add(audio)

        instance.name = name
        instance.can_be_shared = can_be_shared
        instance.save()

        return instance
