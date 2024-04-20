from unittest.mock import call, patch

from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from scrapy.settings import Settings

from backend.models import Item
from backend.tests.utils import TestCaseWithDataMixin
from scraper import settings


class CrawlCommandTests(TestCase):
    def setUp(self) -> None:
        self.crawler_settings = Settings()
        self.crawler_settings.setmodule(settings)

        return super().setUp()

    @patch("scrapy.crawler.CrawlerProcess")
    def test_crawl_all_spiders(self, mock_crawler_process):
        mock_crawler_process.return_value.spider_loader.list.return_value = [
            "spider_1",
            "spider_2",
            "spider_3",
        ]

        call_command("crawl")

        self.assertTrue(mock_crawler_process.called)
        mock_crawler_process.assert_called_with(settings=self.crawler_settings)

        mock_crawler_process().crawl.assert_any_call("spider_1")
        mock_crawler_process().crawl.assert_any_call("spider_2")
        mock_crawler_process().crawl.assert_any_call("spider_3")
        mock_crawler_process().start.assert_called()

        call_command("crawl", "--spider=spider_1")

        self.assertTrue(mock_crawler_process.called)
        mock_crawler_process.assert_called_with(settings=self.crawler_settings)

        mock_crawler_process().crawl.assert_has_calls(
            [call("spider_1"), call("spider_2"), call("spider_3"), call("spider_1")]
        )
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
