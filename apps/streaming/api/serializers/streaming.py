from apps.streaming.models import Audio
from rest_framework import serializers


class StreamingSerializer(serializers.ModelSerializer):
    cover_url = serializers.ReadOnlyField(source="cover_full_url")
    genres = serializers.ReadOnlyField(source="genres_list")

    class Meta:
        model = Audio
        fields = [
            'identifier',
            'name',
            'album',
            'artist',
            'year',
            'genres',
            'cover_url',
            'file_url',
            'duration_in_seconds',
            'md5',
            'created_at',
            'updated_at'
        ]