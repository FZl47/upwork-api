from django.contrib.auth import get_user_model

from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework import permissions as base_permissions
from rest_framework.exceptions import APIException, ValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView as _TokenObtainPairView,
    TokenRefreshView as _TokenRefreshView,
)

from apps.core.swagger import SwaggerViewMixin

from . import serializers, models

User = get_user_model()


class Signup(SwaggerViewMixin, APIView):
    """
        signup user
    """
    swagger_title = 'Signup user'
    swagger_tags = ['Account']
    serializer = serializers.BaseSignupUserSerializer
    serializer_response = serializers.TokenResponseSerializer
    permission_classes = (base_permissions.AllowAny,)

    USER_ROLE_AVAILABLE = models.BaseUser.USER_ROLE_AVAILABLE

    def get_serializer_by_role(self, role):
        if role == 'client':
            return serializers.SignupClientUserSerializer
        else:
            return serializers.SignupFreelancerUserSerializer

    def post(self, request, role):
        if role not in self.USER_ROLE_AVAILABLE:
            raise ValidationError('There is no role with this name %s' % role)

        serializer = self.get_serializer_by_role(role)

        s = serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        tokens = RefreshToken.for_user(user)
        tokens_dict = {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }
        return Response(self.serializer_response(tokens_dict).data, status=status.HTTP_201_CREATED)


class TokenRefresh(SwaggerViewMixin, _TokenRefreshView):
    """
        get access token by refresh token(update login)
    """
    swagger_title = 'Token refresh'
    swagger_tags = ['Account']
    serializer_response = serializers.AccessTokenSerializer
    permission_classes = (base_permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        return super(TokenRefresh, self).post(request, *args, **kwargs)


class Logout(SwaggerViewMixin, APIView):
    """
        need to destroy access token from client side
    """
    swagger_title = 'Logout'
    swagger_tags = ['Account']
    serializer = serializers.RefreshTokenSerializer
    serializer_response = serializers.MessageSerializer

    def delete(self, request, *args, **kwargs):
        # add refresh token to blacklist
        ser = self.serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        refresh_token = ser.validated_data['refresh']
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            pass
        return Response(serializers.MessageSerializer({'message': 'Bye..'}).data)


class Login(SwaggerViewMixin, _TokenObtainPairView):
    """
        get token pair(access & refresh tokens) after user/password validation
    """

    swagger_title = 'Login'
    swagger_tags = ['Account']
    serializer = serializers.LoginSerializer
    serializer_response = serializers.TokenResponseSerializer
    permission_classes = (base_permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise APIException('User not found', code=404)

        if not user.check_password(password):
            raise APIException('Password is wrong', code=400)

        tokens = RefreshToken.for_user(user)
        tokens_dict = {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }
        return Response(self.serializer_response(tokens_dict).data, status=status.HTTP_200_OK)
