# Generated by Django 5.0.3 on 2024-07-08 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0008_alter_payment_table"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="is_close",
            new_name="is_closed",
        ),
    ]
