from apps.catuser.models import CatUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CatUser
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CatUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if "email" in validated_data:
            del validated_data['email']

        if "password" in validated_data:
            del validated_data['password']

        return CatUser.objects.filter(id=instance.id).update(**validated_data)

