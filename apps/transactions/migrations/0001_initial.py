# Generated by Django 5.0.3 on 2024-04-18 17:27

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0008_alter_product_price"),
        ("tables", "0002_alter_table_code"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
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
                        max_length=6,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator("^[0-9A-Z]{6}+$")
                        ],
                    ),
                ),
                (
                    "status",
                    models.TextField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("DELIVERED", "Delivered"),
                            ("CANCELED", "Canceled"),
                        ],
                        default="PENDING",
                        verbose_name="Status",
                    ),
                ),
                (
                    "issued_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date/Time"),
                ),
                (
                    "is_close",
                    models.BooleanField(
                        default=False, verbose_name="Is the order close?"
                    ),
                ),
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
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="orders",
                        to="products.product",
                    ),
                ),
                (
                    "table",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="orders",
                        to="tables.table",
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
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
                "permissions": [
                    ("create_order", "Create order"),
                    ("list_order", "List orders"),
                    ("view_order", "View order"),
                    ("change_order", "Update order"),
                ],
                "abstract": False,
                "default_permissions": (),
            },
        ),
        migrations.AddConstraint(
            model_name="order",
            constraint=models.CheckConstraint(
                check=models.Q(("code__regex", "^[0-9A-Z]{6}+$")),
                name="transactions_order_code_valid",
                violation_error_message="Invalid code.",
            ),
        ),
        migrations.AddConstraint(
            model_name="order",
            constraint=models.CheckConstraint(
                check=models.Q(("status__in", ["PENDING", "DELIVERED", "CANCELED"])),
                name="transactions_order_status_valid",
                violation_error_message="Invalid status.",
            ),
        ),
    ]
