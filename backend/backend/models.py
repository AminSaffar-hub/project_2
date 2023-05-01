from django.db import models

# Create your models here.


class ArticleManager(models.Manager):
    def create_from_body(
        self, name, original_price, reduced_price, location, image, sector, ended_at
    ):
        self.create(
            name=name,
            original_price=original_price,
            reduced_price=reduced_price,
            location=location,
            image=image,
            sector=sector,
            ended_at=ended_at,
        )


class Article(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="Name of the article as scrapped from the provider website.",
    )
    original_price = models.FloatField(
        help_text="Price of the article before reduction"
    )
    reduced_price = models.FloatField(help_text="Price of the article after reduction")
    location = models.URLField(help_text="Url of the article in the provider website")
    image = models.URLField(
        help_text="url to the product image, found in the provider website."
    )

    class ProductSectors(models.Choices):
        FOOD = "food"
        CLOTHES = "clothes"
        SELF_CARE = "self-care"
        APPLIANCES = "appliances"
        COSMETICS = "cosmetics"
        OTHER = "other"

    sector = models.CharField(
        max_length=255,
        choices=ProductSectors.choices,
        help_text="Sector the product belongs to.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=("Date and time when the article promotion ended."),
    )

    objects = ArticleManager()
