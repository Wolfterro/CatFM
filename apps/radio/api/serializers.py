from apps.radio.models import RadioStream
from rest_framework import serializers


class RadioStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioStream
        fields = []
