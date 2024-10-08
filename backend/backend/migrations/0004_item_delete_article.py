# Generated by Django 4.2.1 on 2023-06-13 22:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0003_alter_article_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("title", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("food", "Food"),
                            ("clothes", "Clothes"),
                            ("self-care", "Self Care"),
                            ("appliances", "Appliances"),
                            ("cosmetics", "Cosmetics"),
                            ("other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("description", models.TextField(max_length=2500)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=10, max_digits=6),
                ),
                (
                    "discounted_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "started_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="Date and time when the item promotion started.",
                        null=True,
                    ),
                ),
                (
                    "ended_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="Date and time when the item promotion ended.",
                        null=True,
                    ),
                ),
                (
                    "provider",
                    models.URLField(
                        blank=True, help_text="Url of item provider", null=True
                    ),
                ),
                (
                    "link_to_post",
                    models.URLField(
                        blank=True,
                        help_text="Url of the item in the provider website",
                        null=True,
                    ),
                ),
                (
                    "link_to_image",
                    models.URLField(
                        blank=True,
                        help_text="url to the product image, found in the provider website.",
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Article",
        ),
    ]
