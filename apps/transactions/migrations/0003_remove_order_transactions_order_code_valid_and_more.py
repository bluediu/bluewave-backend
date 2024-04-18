# Generated by Django 5.0.3 on 2024-04-18 18:14

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0008_alter_product_price"),
        ("tables", "0002_alter_table_code"),
        ("transactions", "0002_remove_order_transactions_order_code_valid_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="order",
            name="transactions_order_code_valid",
        ),
        migrations.AlterField(
            model_name="order",
            name="code",
            field=models.CharField(
                max_length=6,
                primary_key=True,
                serialize=False,
                unique=True,
                validators=[django.core.validators.RegexValidator("^[0-9A-Za-z]{6}$")],
            ),
        ),
        migrations.AddConstraint(
            model_name="order",
            constraint=models.CheckConstraint(
                check=models.Q(("code__regex", "^[0-9A-Za-z]{6}$")),
                name="transactions_order_code_valid",
                violation_error_message="Invalid code.",
            ),
        ),
    ]
