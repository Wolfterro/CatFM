from apps.streaming.api.serializers import StreamingSerializer
from apps.streaming.models import DownloadRequest

from apps.streaming.services.downloader import Downloader
from rest_framework import serializers


class DownloadRequestSerializer(serializers.ModelSerializer):
    audio = StreamingSerializer(read_only=True)
    title = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    approved_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DownloadRequest
        fields = [
            'id',
            'audio',
            'title',
            'url',
            'status',
            'created_at',
            'updated_at',
            'approved_at'
        ]

    def create(self, validated_data):
        validated_data['requested_by'] = self.context['request'].user
        download_request = DownloadRequest.objects.create(**validated_data)

        downloader = Downloader([download_request])
        info_list = downloader.get_info()

        try:
            info = info_list[0]
            download_request.title = info.get('title')
            download_request.save()
        except Exception as e:
            print(">>> Erro ao registrar: {}".format(e))
            return None

        return download_request
