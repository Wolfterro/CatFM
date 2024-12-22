from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.streaming.models import Playlist
from apps.streaming.api.serializers.playlist import PlaylistSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = 'identifier'

    allow_any_endpoint_list = []

    def get_permissions(self):
        if self.action in self.allow_any_endpoint_list:
            return [AllowAny()]

        return [IsAuthenticated()]
