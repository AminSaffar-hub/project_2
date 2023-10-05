import math

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=500)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        default=None,
        blank=True,
        null=True,
    )

    description = models.TextField(max_length=2500)
    livraison = models.CharField(
        null=True,
        max_length=20,
        blank=True,
        help_text="The item provider's delivery price",
    )
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=10, blank=True, null=True
    )
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
    last_updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def sale_percentage(self):
        if not self.price or not self.discounted_price:
            return 0
        return math.floor(((self.price - self.discounted_price) / self.price) * 100)

    def __str__(self):
        return self.title + " - " + self.provider_name
