from rest_framework import serializers


class RestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
