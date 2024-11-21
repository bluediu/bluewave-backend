# Core
from functools import partial

# Libs
from rest_framework import serializers as srz
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView as _TokenVerifyView,
)

from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer


_auth_api_schema = partial(extend_schema, tags=["Auth"])


class CustomTokenWithUserInfoSerializer(TokenObtainPairSerializer):
    """Custom token serializer with user information."""

    @classmethod
    def get_token(cls, user):
        """Add user ID to the token."""

        token = super().get_token(user)
        token["user_id"] = user.id
        token["superuser"] = user.is_superuser
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email

        return token

    def validate(self, attrs):
        """Add user ID to the validated data."""

        data = super().validate(attrs)
        data["user_id"] = self.user.id
        data["username"] = self.user.username
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["email"] = self.user.email

        return data


@_auth_api_schema(
    summary="Login",
    responses=OpenApiResponse(
        response=inline_serializer(
            name="LoginOutputSerializer",
            fields={
                "refresh": srz.CharField(),
                "access": srz.CharField(),
            },
        ),
        description="User token successfully retrieved.",
    ),
)
class LoginView(TokenObtainPairView):
    """Log in a user & return the auth tokens."""

    serializer_class = CustomTokenWithUserInfoSerializer


@_auth_api_schema(
    summary="Generate tokens (JWT)",
)
class TokenGenerateView(TokenObtainPairView):
    """Return authentication tokens."""


@_auth_api_schema(
    summary="Renew token (JWT)",
)
class TokenRenewView(TokenRefreshView):
    """Return authentication tokens."""


@_auth_api_schema(
    summary="Verify token (JWT)",
)
class TokenVerifyView(_TokenVerifyView):
    """Check if auth token is valid."""
