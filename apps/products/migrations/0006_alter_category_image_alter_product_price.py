# Generated by Django 5.0.3 on 2024-03-30 18:28

import apps.products.models.category
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                help_text=(
                    "Images must have one of the following extensions: png, jpg, jpeg, webp",
                ),
                unique=True,
                upload_to=apps.products.models.category._image_file_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ["png", "jpg", "jpeg", "webp"]
                    )
                ],
                verbose_name="Image",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.IntegerField(
                help_text="The price of the product must be between $1 USD and $100 USD.",
                validators=[
                    django.core.validators.MinValueValidator(100),
                    django.core.validators.MaxValueValidator(10000),
                ],
                verbose_name="Price",
            ),
        ),
    ]
