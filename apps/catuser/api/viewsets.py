from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError

from apps.catuser.models import CatUser
from apps.catuser.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CatUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]

        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        logged_user = CatUser.objects.get(id=request.user.id)
        if user.id == logged_user.id or logged_user.is_staff:
            return super(UserViewSet, self).destroy(request, *args, **kwargs)

        raise ValidationError({"detail": "Você não tem permissão para deletar outro usuário."})
