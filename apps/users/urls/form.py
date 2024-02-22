from django.urls import path

import apps.users.apis.form as api

users_form_patterns = [
    path("auth/", api.get_auth_form, name="auth"),
]
