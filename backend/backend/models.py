import math

from django.db import models
from django.utils.translation import gettext_lazy as _
import jellyfish
from django.contrib.auth.models import User
import random


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/images/", blank=True, null=True)
    score = models.FloatField(
        null=True,
        blank=True,
        default=1,
        help_text="Evaluation of category importance. Affects display order",
    )

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(
        null=True, max_length=20, blank=True, help_text="The shop's name"
    )
    link = models.URLField(null=True, blank=True, help_text="Url to shop")
    logo = models.ImageField(upload_to="static/images/", blank=True, null=True)
    score = models.FloatField(
        null=True,
        blank=True,
        default=1,
        help_text="Evaluation of offers on shop. Affects display order",
    )


class Item(models.Model):
    title = models.CharField(max_length=500)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        default=None,
        blank=True,
        null=False,
    )

    description = models.TextField(max_length=2500)

    class DeliveryOptions(models.TextChoices):
        AVAILABLE = "available", _("available")
        NOT_AVAILABLE = "not available", _("not available")
        WITH_CONDITONS = "with conditions", _("with conditions")

    delivery = models.CharField(
        null=True,
        max_length=20,
        blank=True,
        choices=DeliveryOptions.choices,
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
    link_to_post = models.URLField(
        null=True, blank=True, help_text="Url of the item in the provider website"
    )
    link_to_image = models.URLField(
        null=True,
        blank=True,
        help_text="url to the product image, found in the provider website.",
    )
    last_updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    provider = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="items",
        default=None,
        blank=True,
        null=True,
    )

    @property
    def sale_percentage(self):
        if not self.price or not self.discounted_price:
            return 0
        return math.floor(((self.price - self.discounted_price) / self.price) * 100)

    def __str__(self):
        return self.title + " - " + self.provider.name

    def similar_items(self, threshold=0.8):
        """
        Return a list of items with similarity scores higher than
        the specified threshold, sorted by similarity score.
        """
        list_of_items = Item.objects.exclude(id=self.pk)
        similarity_scores = {
            item: self.similar(item.title, self.title) for item in list_of_items
        }
        similar_items = [
            item
            for item, score in sorted(
                similarity_scores.items(), key=lambda x: x[1], reverse=True
            )
            if score > threshold
        ]
        list_of_items_same = list(
            Item.objects.exclude(id=self.pk)
            .filter(category=self.category, provider=self.provider)
            .distinct()
        )
        while len(similar_items) < 10 and list_of_items_same:
            similar_items.append(
                list_of_items_same.pop(random.randint(0, len(list_of_items_same) - 1))
            )
        return similar_items[:5]

    @staticmethod
    def similar(a, b):
        """
        Calculate similarity ratio between two strings using SequenceMatcher.
        """
        return jellyfish.jaro_similarity(a, b)


class Like(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="user_likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items_liked")

    def __str__(self):
        return f"{self.user} likes {self.item}"

    class Meta:
        unique_together = ("item", "user")
