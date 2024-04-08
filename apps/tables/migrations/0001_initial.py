# Generated by Django 5.0.3 on 2024-04-09 22:29

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Table",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(editable=False, verbose_name="Created"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(editable=False, verbose_name="Updated"),
                ),
                (
                    "code",
                    models.CharField(
                        help_text="The table code must contain 4 numeric characters and follow a sequence pattern like '000X'.",
                        max_length=4,
                        unique=True,
                        validators=[
                            django.core.validators.MaxValueValidator(4),
                            django.core.validators.MinValueValidator(4),
                        ],
                        verbose_name="Code",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(app_label)s_%(class)s_created_by",
                        related_query_name="%(app_label)s_%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(app_label)s_%(class)s_updated_by",
                        related_query_name="%(app_label)s_%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Table",
                "verbose_name_plural": "Tables",
                "permissions": [
                    ("create_table", "Create table"),
                    ("list_table", "List table"),
                    ("view_table", "View table"),
                    ("change_table", "Change table"),
                ],
                "abstract": False,
                "default_permissions": (),
            },
        ),
        migrations.AddConstraint(
            model_name="table",
            constraint=models.CheckConstraint(
                check=models.Q(("code__ne", "")),
                name="tables_table_code_not_empty_check",
                violation_error_message="Code can't be empty.",
            ),
        ),
        migrations.AddConstraint(
            model_name="table",
            constraint=models.CheckConstraint(
                check=models.Q(("code__regex", "^[0-9]+$")),
                name="tables_table_code_valid",
            ),
        ),
    ]
