from functools import partial

from rest_framework import serializers as srz
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView as _TokenVerifyView,
)


_auth_api_schema = partial(extend_schema, tags=["Auth"])


class CustomTokenWithUserInfoSerializer(TokenObtainPairSerializer):
    """Custom token serializer with user information."""

    @classmethod
    def get_token(cls, user):
        """Add user ID to the token."""
        token = super().get_token(user)
        token["user_id"] = user.id
        return token

    def validate(self, attrs):
        """Add user ID to the validated data."""
        data = super().validate(attrs)
        data["user_id"] = self.user.id
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
