# Generated by Django 5.0.3 on 2024-04-01 01:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_alter_category_image_alter_product_price"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="product",
            name="products_product_price_check",
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.CheckConstraint(
                check=models.Q(("price__gte", 100)), name="products_product_price_check"
            ),
        ),
    ]
