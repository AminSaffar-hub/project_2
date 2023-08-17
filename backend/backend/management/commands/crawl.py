from django.core.management.base import BaseCommand
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from scraper.spiders.beautystore import BeautyStoreSpider
from scraper.spiders.cosmetique import CosmetiqueSpider
from scraper.spiders.exist import ExistSpider
from scraper.spiders.zara import ZaraSpider
from scraper.spiders.mg import MgSpider
from scraper.spiders.tunisianet import TunisiaNetSpider
from scraper.spiders.tdiscount import TdiscountSpider
from scraper import settings


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(TdiscountSpider)
        process.crawl(MgSpider)
        process.crawl(ZaraSpider)
        process.crawl(TunisiaNetSpider)
        process.crawl(ExistSpider)
        process.crawl(BeautyStoreSpider)
        process.crawl(CosmetiqueSpider)
        process.start()
