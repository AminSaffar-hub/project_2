from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from backend.models import Item

EXPIRATION_DATE_IN_DAYS = 3


class Command(BaseCommand):
    help = "delete items that haven't been updated since 3 days"

    def handle(self, *args, **options):
        threshold_date = timezone.now() - timedelta(days=EXPIRATION_DATE_IN_DAYS)
        expired_items = Item.objects.filter(last_updated_at__lt=threshold_date)
        expired_items.delete()
