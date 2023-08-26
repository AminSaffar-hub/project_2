import scrapy
from scraper.items import ArticleItem
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CosmetiqueSpider(CrawlSpider):
    name = "cosmetique"
    allowed_domains = ["cosmetique.tn"]
    start_urls = ["https://cosmetique.tn/promotions?page=1"]
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
        item["title"] = response.css(".product-title::text").getall()
        item["discounted_price"] = response.css("span.price::text").get()
        item["price"] = response.css(".regular-price::text").get()
        item["link_to_post"] = response.url
        item["link_to_image"] = response.css(".js-qv-product-cover::attr(src)").get()
        item["category"] = "cosmetics"
        item["description"] = response.css(
            '[id^="product-description-"] *::text'
        ).extract()
        item["provider_name"] = "cosmetique"
        item["link_to_provider"] = "https://cosmetique.tn"
        item["livraison"] = "sous condition"
        item["online_payment"] = True

        yield item

    def fetch_items(self, response):
        if response.status == 404:
            raise CloseSpider("No more pages, quitting !!")

        items = response.css(
            "article.product-miniature div div h3 a::attr(href)"
        ).getall()

        if not len(items):
            raise CloseSpider(f"Empty page {self.page_number}, quitting !!")

        for article_url in items:
            yield scrapy.Request(
                url=response.urljoin(article_url),
                callback=self.parse_item,
            )
        self.page_number += 1
        next_page = f"https://cosmetique.tn/promotions?page={self.page_number}"
        yield response.follow(next_page, callback=self.fetch_items)
