import threading

from apps.streaming.api.serializers import StreamingSerializer
from apps.streaming.models import DownloadRequest

from rest_framework import serializers


class DownloadRequestSerializer(serializers.ModelSerializer):
    audio = StreamingSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    approved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DownloadRequest
        fields = [
            'id',
            'audio',
            'url',
            'status',
            'created_at',
            'updated_at',
            'approved_at'
        ]

    def create(self, validated_data):
        if DownloadRequest.objects.filter(url=validated_data['url']).exists():
            raise serializers.ValidationError({"message": "Já existe uma requisição com esse link."})

        validated_data['requested_by'] = self.context['request'].user
        download_request = DownloadRequest.objects.create(**validated_data)
        threading.Thread(target=download_request.set_info).start()

        return download_request
