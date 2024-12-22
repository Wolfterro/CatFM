from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.streaming.models import Audio
from apps.streaming.api.serializers.streaming import StreamingSerializer


class StreamingViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.filter(is_active=True)
    serializer_class = StreamingSerializer
    lookup_field = 'identifier'
    http_method_names = ['get', 'head', 'options']

    allow_any_endpoint_list = []

    def get_permissions(self):
        if self.action in self.allow_any_endpoint_list:
            return [AllowAny()]

        return [IsAuthenticated()]
