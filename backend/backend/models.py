import math

from django.db import models

# Create your models here.


class ArticleManager(models.Manager):
    def create_from_body(
        self, name, old_price, new_price, url, image_link, type, description
    ):
        self.create(
            name=name,
            old_price=old_price,
            new_price=new_price,
            url=url,
            image_link=image_link,
            type=type,
            description=description,
        )


class Article(models.Model):
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Name of the article as scrapped from the provider website.",
    )
    old_price = models.FloatField(
        null=True, blank=True, help_text="Price of the article before reduction"
    )
    new_price = models.FloatField(
        null=True, blank=True, help_text="Price of the article after reduction"
    )
    url = models.URLField(
        null=True, blank=True, help_text="Url of the article in the provider website"
    )
    image_link = models.URLField(
        null=True,
        blank=True,
        help_text="url to the product image, found in the provider website.",
    )

    class ProductType(models.Choices):
        FOOD = "food"
        CLOTHES = "clothes"
        SELF_CARE = "self-care"
        APPLIANCES = "appliances"
        COSMETICS = "cosmetics"
        OTHER = "other"

    type = models.CharField(
        default=None,
        max_length=255,
        choices=ProductType.choices,
        help_text="Sector the product belongs to.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    description = models.TextField(
        null=True,
        blank=True,
        help_text="details about the article and the promotion",
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=("Date and time when the article promotion ended."),
    )

    objects = ArticleManager()

    @property
    def percentage(self):
        if not self.old_price or not self.new_price:
            return 0
        return math.floor(((self.old_price - self.new_price) / self.old_price) * 100)
