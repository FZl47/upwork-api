from rest_framework import serializers

from . import models


class BaseSignupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseUser
        fields = (
            'password', 'username', 'first_name', 'last_name', 'email'
        )


class SignupClientUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=10)

    class Meta:
        model = models.ClientUser
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password', 'role', 'is_active'
        )

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class SignupFreelancerUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=10)

    class Meta:
        model = models.FreelancerUser
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password', 'role', 'is_active'
        )

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


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
