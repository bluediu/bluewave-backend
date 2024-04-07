# Generated by Django 5.0.3 on 2024-04-03 21:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_remove_product_products_product_price_check_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.IntegerField(
                help_text="The price of the product must be between $1.00 USD and $100.00 USD.",
                validators=[
                    django.core.validators.MinValueValidator(100),
                    django.core.validators.MaxValueValidator(10000),
                ],
                verbose_name="Price",
            ),
        ),
    ]
