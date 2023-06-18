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
        item = ArticleItem()
        item["title"] = response.css("h1.h1::text").getall()
        item["discounted_price"] = response.css(".cart-price-value::text").get()
        item["price"] = response.css(".cart-price-discount::text").get()
        item["link_to_post"] = response.url
        item["link_to_image"] = response.css(".js-qv-product-cover::attr(src)").get()
        item["category"] = "cosmetics"
        item["description"] = response.css(
            '[id^="product-description-"] p::text'
        ).extract()
        item["provider_name"] = "beautystore"
        item["link_to_provider"] = "https://beautystore.tn"
        item["livraison"] = "sous condition"
        item["online_payment"] = True
        
        yield item

    def fetch_item(self, response):
        if response.status == 404:
            raise CloseSpider("No more pages, quitting !!")

        items = response.css("article.product-miniature div a::attr(href)").getall()

        if not len(items):
            raise CloseSpider(f"Empty page {self.page_number}, quitting !!")

        for article_url in items:
            yield scrapy.Request(
                url=response.urljoin(article_url),
                callback=self.parse_item,
            )
        self.page_number += 1
        next_page = f"https://beautystore.tn/164-promos?page={self.page_number}"
        yield response.follow(next_page, callback=self.fetch_item)
