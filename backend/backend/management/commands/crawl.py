from django.core.management.base import BaseCommand, CommandError
from scraper import settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


class Command(BaseCommand):
    help = "Release the spiders"

    def add_arguments(self, parser):
        parser.add_argument("-s", "--spider", type=str, help="Provide a spider name")

    def handle(self, *args, **options):
        scraper_settings = Settings()
        scraper_settings.setmodule(settings)
        process = CrawlerProcess(settings=scraper_settings)
        all_spiders = process.spider_loader.list()
        spider_by_user = options["spider"]

        if spider_by_user and spider_by_user not in all_spiders:
            raise CommandError("Please provide a valid value for your_argument.")

        if spider_by_user:
            spiders_to_run = [spider_by_user]
        else:
            spiders_to_run = all_spiders

        for spider_name in spiders_to_run:
            process.crawl(spider_name)
        process.start()
