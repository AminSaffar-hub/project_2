from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from scrapy.settings import Settings

from scraper import settings


class CrawlCommandTests(TestCase):
    @patch("scraper.spiders.beautystore.BeautyStoreSpider")
    @patch("scrapy.crawler.CrawlerProcess")
    def test_spider_release(self, mock_crawler_process, mock_beauty_store_spider):
        # Call the management command
        call_command("crawl")

        crawler_settings = Settings()
        crawler_settings.setmodule(settings)

        # Assertions
        self.assertTrue(mock_crawler_process.called)
        mock_crawler_process.assert_called_with(settings=crawler_settings)
        mock_crawler_process().crawl.assert_called_with(mock_beauty_store_spider)
        mock_crawler_process().start.assert_called()
