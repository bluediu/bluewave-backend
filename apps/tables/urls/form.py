from django.urls import path

import apps.tables.apis.form as api

tables_form_patterns = [
    path("create/", api.get_create_table_form, name="create"),
    path(
        "<int:table_id>/update/",
        api.get_update_table_form,
        name="update",
    ),
]
