from rest_framework import viewsets

from apps.catuser.models import CatUser
from apps.catuser.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CatUser.objects.all()
    serializer_class = UserSerializer
