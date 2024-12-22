from django_filters import rest_framework as filters
from apps.streaming.models import Audio


class StreamingFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')  # Busca parcial no nome
    album = filters.CharFilter(lookup_expr='icontains')  # Busca parcial no album
    artist = filters.CharFilter(lookup_expr='icontains')  # Busca parcial no artista
    year = filters.NumberFilter()

    created_at = filters.DateFilter()  # Filtra pela data de criação
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')  # Criado antes
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')  # Criado depois

    class Meta:
        model = Audio
        fields = ['name', 'album', 'artist', 'year', 'created_at', 'created_before', 'created_after']
