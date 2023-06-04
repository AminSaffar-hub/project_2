import scrapy
from scraper.items import ArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.exceptions import CloseSpider


class BeautyStoreSpider(CrawlSpider):
    name = "beautystore"
    allowed_domains = ["beautystore.tn"]
    start_urls = [
        "https://beautystore.tn/164-promos?page=1",
    ]
    rules = [
        Rule(
            LinkExtractor(allow=r"164-promos\?page=\d+"),
            callback="fetch_item",
            follow=True,
        )
    ]
    page_number = 1

    def parse_item(self, response):
        article = ArticleItem()
        article["name"] = response.css("h1.h1::text").getall()
        article["new_price"] = response.css(".cart-price-value::text").get()
        article["old_price"] = response.css(".cart-price-discount::text").get()
        article["url"] = response.url
        article["image_link"] = response.css(".js-qv-product-cover::attr(src)").get()
        article["type"] = "cosmetics"
        article["description"] = response.css(
            '[id^="product-description-"] p::text'
        ).extract()
        yield article

    def fetch_item(self, response):
        if response.status == 404:
            raise CloseSpider("No more pages, quitting !!")

        articles = response.css("article.product-miniature div a::attr(href)").getall()

        if not len(articles):
            raise CloseSpider(f"Empty page {self.page_number}, quitting !!")

        for article_url in articles:
            yield scrapy.Request(
                url=response.urljoin(article_url),
                callback=self.parse_item,
            )
        self.page_number += 1
        next_page = f"https://beautystore.tn/164-promos?page={self.page_number}"
        yield response.follow(next_page, callback=self.fetch_item)
