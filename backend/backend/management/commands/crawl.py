from django.core.management.base import BaseCommand
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from scraper.spiders.beautystore import BeautyStoreSpider
from scraper.spiders.cosmetique import CosmetiqueSpider
from scraper.spiders.exist import ExistSpider
from scraper import settings

from backend.models import Item


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        Item.objects.all().delete()
        crawler_settings = Settings()
        crawler_settings.setmodule(settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(ExistSpider)
        process.crawl(BeautyStoreSpider)
        process.crawl(CosmetiqueSpider)
        process.start()
