import scrapy
from scrapy.exceptions import CloseSpider

from backend.models import Item
from scraper.items import ArticleItem


class BeautyStoreSpider(scrapy.Spider):
    name = "beautystore"
    allowed_domains = ["beautystore.tn"]
    start_urls = [
        "https://beautystore.tn/164-promos?page=1",
    ]
    page_number = 1
    category_names = []  # List to store category names

    def parse(self, response):
        try:
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
            yield response.follow(next_page, callback=self.parse)
        except Exception as e:
            print(f"Error in parse: {e}")

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
        item["provider"] = "Beauty Store"
        item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
        item["online_payment"] = True
        category_name = response.url
        print(category_name)
        self.category_names.append(category_name)  # Append category name to the list
        yield item

    def closed(self, reason):
        # This method is called when the spider is closed
        print("Category Names:", set(self.category_names))
