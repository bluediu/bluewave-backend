# Libs
from django.urls import include, path

# Apps
import apps.users.apis.user as api

users_patterns = [
    path("list/", api.get_users, name="list"),
    path("create/", api.create_user, name="create"),
    path(
        "<int:user_id>/",
        include(
            [
                path("get/", api.get_user, name="get"),
                path("update/", api.update_user, name="update"),
            ]
        ),
    ),
]
