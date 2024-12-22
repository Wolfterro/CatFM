from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.streaming.api.filters import StreamingFilter
from apps.streaming.models import Audio
from apps.streaming.api.serializers.streaming import StreamingSerializer


class StreamingViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.filter(is_active=True)
    serializer_class = StreamingSerializer
    lookup_field = 'identifier'
    http_method_names = ['get', 'head', 'options']
    filterset_class = StreamingFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    allow_any_endpoint_list = []

    def get_permissions(self):
        if self.action in self.allow_any_endpoint_list:
            return [AllowAny()]

        return [IsAuthenticated()]
