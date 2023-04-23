# Generated by Django 4.2 on 2023-04-23 18:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
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
                    "name",
                    models.CharField(
                        help_text="Name of the article as scrapped from the provider website.",
                        max_length=255,
                    ),
                ),
                (
                    "original_price",
                    models.FloatField(
                        help_text="Price of the article before reduction"
                    ),
                ),
                (
                    "reduced_price",
                    models.FloatField(help_text="Price of the article after reduction"),
                ),
                (
                    "location",
                    models.URLField(
                        help_text="Url of the article in the provider website"
                    ),
                ),
                (
                    "image",
                    models.URLField(
                        help_text="url to the product image, found in the provider website."
                    ),
                ),
                (
                    "sector",
                    models.CharField(
                        choices=[
                            ("food", "Food"),
                            ("clothes", "Clothes"),
                            ("self-care", "Self Care"),
                            ("appliances", "Appliances"),
                            ("other", "Other"),
                        ],
                        help_text="Sector the product belongs to.",
                        max_length=255,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "ended_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="Date and time when the article promotion ended.",
                        null=True,
                    ),
                ),
            ],
        ),
    ]
