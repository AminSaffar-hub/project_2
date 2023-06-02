import scrapy
from scraper.items import ArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class BeautyStoreSpider(CrawlSpider):
    name = "beautystore"
    allowed_domains = ["beautystore.tn"]
    start_urls = [
        "https://beautystore.tn/164-promos?page=1",
        "https://beautystore.tn/164-promos?page=2",
    ]
    rules = [
        Rule(
            LinkExtractor(allow=r"164-promos\?page=\d+"),
            callback="fetch_item",
            follow=True,
        )
    ]

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
        for article_url in response.css(
            "article.product-miniature div a::attr(href)"
        ).getall():
            yield scrapy.Request(
                url=response.urljoin(article_url),
                callback=self.parse_item,
            )
