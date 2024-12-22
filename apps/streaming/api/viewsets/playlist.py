from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.streaming.models import Playlist
from apps.streaming.api.serializers.playlist import PlaylistSerializer
from apps.streaming.api.filters.playlist import PlaylistFilter


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    lookup_field = 'identifier'
    filterset_class = PlaylistFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'created_at', 'updated_at']

    allow_any_endpoint_list = []

    def get_permissions(self):
        if self.action in self.allow_any_endpoint_list:
            return [AllowAny()]

        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_playlists(self, request):
        user = request.user
        queryset = Playlist.objects.filter(owner=user)
        filterset = PlaylistFilter(request.GET, queryset=queryset, request=request)
        data = PlaylistSerializer(filterset.qs, many=True).data

        return Response(data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def system_playlists(self, request):
        queryset = Playlist.objects.filter(is_system_playlist=True)
        filterset = PlaylistFilter(request.GET, queryset=queryset, request=request)
        data = PlaylistSerializer(filterset.qs, many=True).data

        return Response(data)
