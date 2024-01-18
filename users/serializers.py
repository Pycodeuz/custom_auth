from django.contrib.auth import get_user_model
# serializers.py
from rest_framework import serializers

from .models import User


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone', 'password',
                  'is_superuser', 'is_active', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        instance.email = validated_data.get('email', instance.email)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class GenerateNewSerializer(serializers.Serializer):
    email = serializers.EmailField()

