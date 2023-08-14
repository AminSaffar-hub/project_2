from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraper import settings
from scraper.spiders.beautystore import BeautyStoreSpider
from scraper.spiders.cosmetique import CosmetiqueSpider
from scraper.spiders.exist import ExistSpider


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(ExistSpider)
        process.crawl(BeautyStoreSpider)
        process.crawl(CosmetiqueSpider)
        process.start()
