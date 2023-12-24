from django.urls import path, include

from apps.users.urls.auth import auth_patterns
from apps.users.urls.user import users_patterns

app_name = "users"


urlpatterns = [
    path("auth/", include((auth_patterns, app_name), namespace="auth")),
    path("user/", include((users_patterns, app_name), namespace="user")),
]
