# Libs
from django.urls import path, include

# Apps
from apps.users.apis import auth

auth_patterns = [
    path("login/", auth.LoginView.as_view(), name="token_obtain_pair"),
    path(
        "jwt/",
        include(
            [
                path(
                    "generate/", auth.TokenGenerateView.as_view(), name="generate_token"
                ),
                path("renew/", auth.TokenRenewView.as_view(), name="renew_token"),
                path("verify/", auth.TokenVerifyView.as_view(), name="verify_token"),
            ]
        ),
    ),
]
