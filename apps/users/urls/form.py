from django.urls import path, include

import apps.users.apis.form as api

users_form_patterns = [
    path("auth/", api.get_auth_form, name="auth"),
    path("create/", api.get_create_user_form, name="create"),
    path("<int:user_id>/update/", api.get_update_user_form, name="update"),
]
