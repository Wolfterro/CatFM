from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.streaming.api.serializers.download_request import DownloadRequestSerializer
from apps.streaming.models import DownloadRequest


class DownloadRequestViewSet(viewsets.ModelViewSet):
    queryset = DownloadRequest.objects.none()
    serializer_class = DownloadRequestSerializer
    http_method_names = ['post', 'head', 'options']

    allow_any_endpoint_list = []

    def get_permissions(self):
        if self.action in self.allow_any_endpoint_list:
            return [AllowAny()]

        return [IsAuthenticated()]
