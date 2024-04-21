import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from backend.models import Item
from scraper.items import ArticleItem

category_mapping = {
    "clothes": [
        "casquettes",
        "lunettes",
        "ceintures",
        "gilets",
        "t-shirts",
        "pantalons",
        "pulls-polos",
        "shorts",
        "bermudas",
        "pantalons-de-ville",
        "parapluies",
        "sweats",
        "bracelets",
        "portefeuilles",
        "mocassins",
        "echarpes",
        "boots",
        "manteaux",
        "blazers",
        "derbies",
        "jeans",
        "baskets",
        "chemises",
        "pantacourts",
        "polos",
        "pullovers",
        "sacs",
        "cravates",
        "montres",
        "shorts-bermudas",
        "joggers",
        "costumes-blazers",
        "pulls",
        "slacks",
        "mules",
        "blousons",
        "shorts-maillots",
    ]
}


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
        reverse_mapping = {
            value: key for key, values in category_mapping.items() for value in values
        }
        category_name = response.url.split("/")[3]
        associated_key = reverse_mapping.get(category_name)
        if associated_key:
            item["category"] = associated_key
        else:
            item["category"] = "other"
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
