from django.core.management.base import BaseCommand
from scraper import settings
from scraper.spiders.beautystore import BeautyStoreSpider
from scraper.spiders.cosmetique import CosmetiqueSpider
from scraper.spiders.exist import ExistSpider
from scraper.spiders.mg import MgSpider
from scraper.spiders.tdiscount import TdiscountSpider
from scraper.spiders.citywatch import CitywatchSpider
from scraper.spiders.tunisianet import TunisiaNetSpider
from scraper.spiders.zara import ZaraSpider
from scraper.spiders.monoprix import MonoprixSpider
from scraper.spiders.tunisiatech import TunisiatechSpider
from scraper.spiders.peak import PeakSpider

from scraper.spiders.chillandlit import chillandlit
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(PeakSpider)
        #process.crawl(CitywatchSpider)
        #process.crawl(TunisiatechSpider)
        #process.crawl(chillandlit)
        #process.crawl(TdiscountSpider)
        #process.crawl(MonoprixSpider)
        #process.crawl(MgSpider)
        #process.crawl(ZaraSpider)
        #process.crawl(TunisiaNetSpider)
        #process.crawl(ExistSpider)
        #process.crawl(BeautyStoreSpider)
        #process.crawl(CosmetiqueSpider)
        process.start()
