from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers


class RestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name',)

    # def update(self, validated_data):
    #     print(validated_data)
    #     user = User.objects.create_user(
    #         **validated_data
    #     )
    #     return user

