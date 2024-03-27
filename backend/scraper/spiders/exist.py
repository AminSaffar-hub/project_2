import scrapy
from scraper.items import ArticleItem
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from backend.models import Item


class ExistSpider(CrawlSpider):
    name = "exist"
    allowed_domains = ["www.exist.com.tn"]
    start_urls = ["https://www.exist.com.tn/promotions?page=1"]

    rules = [
        Rule(
            LinkExtractor(allow=r"promotions\?page=\d+"),
            callback="fetch_items",
            follow=True,
        )
    ]
    page_number = 1

    def parse_item(self, response):
        item = ArticleItem()
        item["title"] = response.css(".h1-main::text").getall()
        item["discounted_price"] = response.css(".current-price span::text").get()
        item["price"] = response.css(".regular-price::text").get()
        item["link_to_post"] = response.url
        item["link_to_image"] = response.css(".js-qv-product-cover::attr(src)").get()
        item["description"] = response.css(
            '[id^="product-description-"] *::text'
        ).extract()
        item["provider"] = "Exist"
        item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
        item["online_payment"] = True

        yield item

    def fetch_items(self, response):
        if response.status == 404:
            raise CloseSpider("No more pages, quitting !!")

        items = response.css("li.product_item div div a::attr(href)").getall()

        if not len(items):
            raise CloseSpider(f"Empty page {self.page_number}, quitting !!")

        for article_url in items:
            yield scrapy.Request(
                url=response.urljoin(article_url),
                callback=self.parse_item,
            )
        self.page_number += 1
        next_page = f"https://www.exist.com.tn/promotions?page={self.page_number}"
        yield response.follow(next_page, callback=self.fetch_items)
