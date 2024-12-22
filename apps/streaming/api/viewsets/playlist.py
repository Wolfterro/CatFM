from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_playlists(self, request):
        user = request.user
        queryset = Playlist.objects.filter(owner=user)
        data = PlaylistSerializer(queryset, many=True).data

        return Response(data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def system_playlists(self, request):
        queryset = Playlist.objects.filter(is_system_playlist=True)
        data = PlaylistSerializer(queryset, many=True).data

        return Response(data)
