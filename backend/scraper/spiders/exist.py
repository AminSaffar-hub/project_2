import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.exceptions import CloseSpider

from scraper.items import ArticleItem


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
        article = ArticleItem()
        article["name"] = response.css(".h1-main::text").getall()
        article["new_price"] = response.css(".current-price span::text").get()
        article["old_price"] = response.css(".regular-price::text").get()
        article["url"] = response.url
        article["image_link"] = response.css(".js-qv-product-cover::attr(src)").get()
        article["type"] = "clothes"
        article["description"] = response.css(
            '[id^="product-description-"] *::text'
        ).extract()
        yield article

    def fetch_items(self, response):
        if response.status == 404:
            raise CloseSpider("No more pages, quitting !!")

        articles = response.css("li.product_item div div a::attr(href)").getall()

        if not len(articles):
            raise CloseSpider(f"Empty page {self.page_number}, quitting !!")

        for article_url in articles:
            yield scrapy.Request(
                url=response.urljoin(article_url),
                callback=self.parse_item,
            )
        self.page_number += 1
        next_page = f"https://www.exist.com.tn/promotions?page={self.page_number}"
        yield response.follow(next_page, callback=self.fetch_item)
