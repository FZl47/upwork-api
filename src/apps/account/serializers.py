from rest_framework import serializers

from . import models


class BaseSignupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseUser
        fields = (
            'password', 'username', 'first_name', 'last_name', 'email'
        )


class SignupClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientUser
        fields = '__all__'


class SignupFreelancerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FreelancerUser
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    access = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
