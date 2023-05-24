from django.core.management.base import BaseCommand
from backend.scrapping.run_scrapping import run_scrapping


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            run_scrapping()
        except Exception as e:
            print(e)
