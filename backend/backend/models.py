import math

from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=100)

    class ItemCategories(models.Choices):
        FOOD = "food"
        CLOTHES = "clothes"
        SELF_CARE = "self-care"
        APPLIANCES = "appliances"
        COSMETICS = "cosmetics"
        OTHER = "other"

    category = models.CharField(choices=ItemCategories.choices, max_length=50)
    description = models.TextField(max_length=2500)
    livraison = models.CharField(null=True, max_length=20, blank=True, help_text="The item provider's delivery price")
    price = models.DecimalField(max_digits=6, decimal_places=2, default=10)
    online_payment = models.BooleanField(default=False)
    discounted_price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=("Date and time when the item promotion started."),
    )
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=("Date and time when the item promotion ended."),
    )

    provider_name = models.CharField(
        null=True, max_length=20, blank=True, help_text="The item provider's name"
    )
    link_to_provider = models.URLField(
        null=True, blank=True, help_text="Url of item provider"
    )
    link_to_post = models.URLField(
        null=True, blank=True, help_text="Url of the item in the provider website"
    )
    link_to_image = models.URLField(
        null=True,
        blank=True,
        help_text="url to the product image, found in the provider website.",
    )

    @property
    def sale_percentage(self):
        if not self.price or not self.discounted_price:
            return 0
        return math.floor(((self.price - self.discounted_price) / self.price) * 100)
