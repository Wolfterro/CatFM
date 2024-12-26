import os

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.radio.models import RadioStream
from apps.radio.api.serializers import RadioStreamSerializer


class RadioStreamViewSet(viewsets.ModelViewSet):
    queryset = RadioStream.objects.none()
    serializer_class = RadioStreamSerializer
    allow_any_endpoint_list = []

    http_method_names = ['get', 'head', 'options']

    def get_permissions(self):
        if self.action in self.allow_any_endpoint_list:
            return [AllowAny()]

        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        raise ValidationError({"message": "Você nao possui permissão para listar as transmissões."})

    def retrieve(self, request, *args, **kwargs):
        raise ValidationError({"message": "Você nao possui permissão para visualizar uma transmissão."})

    def create(self, request, *args, **kwargs):
        raise ValidationError({"message": "Você nao possui permissão para criar uma transmissão."})

    def update(self, request, *args, **kwargs):
        raise ValidationError({"message": "Você nao possui permissão para editar uma transmissão."})

    def destroy(self, request, *args, **kwargs):
        raise ValidationError({"message": "Você nao possui permissão para deletar uma transmissão."})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def stop_broadcast(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            pid = request.GET.get('pid')
            try:
                os.kill(int(pid), 9)
                return Response({"success": True, "pid": pid})
            except Exception as e:
                return Response({"success": False, "pid": pid, "error": str(e)})

        raise ValidationError({"message": "Você não possui permissão para encerrar a transmissão."})
