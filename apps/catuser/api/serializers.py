from apps.catuser.models import CatUser
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CatUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff']
