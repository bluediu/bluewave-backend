# Generated by Django 5.0.3 on 2024-07-23 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0009_rename_is_close_order_is_closed"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="orders",
                to="transactions.payment",
            ),
        ),
    ]
