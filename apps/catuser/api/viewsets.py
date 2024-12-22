from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.catuser.models import CatUser
from apps.catuser.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CatUser.objects.all()
    serializer_class = UserSerializer
    allow_any_endpoint_list = ['login', 'create']

    def get_permissions(self):
        if self.action in self.allow_any_endpoint_list:
            return [AllowAny()]

        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        logged_user = CatUser.objects.get(id=request.user.id)
        if user.id == logged_user.id or logged_user.is_staff:
            return super(UserViewSet, self).destroy(request, *args, **kwargs)

        raise ValidationError({"detail": "Você não tem permissão para deletar outro usuário."})

    # Custom Endpoints
    # ----------------
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        user = CatUser.objects.filter(email=request.data['email'], is_active=True).first()
        if not user:
            raise ValidationError({"detail": "Credenciais inválidas."})

        if user.check_password(request.data['password']):
            data = UserSerializer(user).data
            data['token'] = user.auth_token.key
            return Response(data)

        raise ValidationError({"detail": "Credenciais inválidas."})

    @action(detail=True, methods=['patch'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        if user.id != request.user.id or not request.user.is_staff:
            raise ValidationError({"detail": "Você não tem permissão para editar outro usuário."})

        user.set_password(request.data['password'])
        user.save()
        return Response({"success": True})
