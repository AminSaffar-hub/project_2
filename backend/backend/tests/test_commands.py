from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from scrapy.settings import Settings

from backend.models import Item
from backend.tests.utils import TestCaseWithDataMixin
from scraper import settings


class CrawlCommandTests(TestCase):
    @patch("scraper.spiders.cosmetique.CosmetiqueSpider")
    @patch("scrapy.crawler.CrawlerProcess")
    def test_spider_release(self, mock_crawler_process, mock_cosmetique_spider):
        # Call the management command
        call_command("crawl")

        crawler_settings = Settings()
        crawler_settings.setmodule(settings)

        # Assertions
        self.assertTrue(mock_crawler_process.called)
        mock_crawler_process.assert_called_with(settings=crawler_settings)
        mock_crawler_process().crawl.assert_called_with(mock_cosmetique_spider)
        mock_crawler_process().start.assert_called()


@freeze_time("2023-07-19 12:00:00")
class DeleteExpiredItemsTests(TestCaseWithDataMixin, TestCase):
    @freeze_time("2023-07-23 12:00:00")
    def test_delete_expired_items(self):
        call_command("delete_expired_items")
        self.assertEquals(Item.objects.all().count(), 0)

    @freeze_time("2023-07-23 12:00:00")
    def test_delete_items_with_none_update_time(self):
        self.item1.last_updated_at = None
        self.item1.save()

        call_command("delete_expired_items")
        self.assertEquals(Item.objects.all().count(), 0)
