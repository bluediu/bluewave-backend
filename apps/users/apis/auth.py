from functools import partial

from rest_framework import serializers as srz
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView as _TokenVerifyView,
)


_auth_api_schema = partial(extend_schema, tags=["Auth"])


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
