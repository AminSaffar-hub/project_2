import scrapy
from scraper.items import ArticleItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule


class BeautystoreSpider(scrapy.Spider):
    name = "beautystore"
    allowed_domains = ["beautystore.tn"]
    start_urls = ["https://beautystore.tn/"]
    rules = [
        Rule(
            LinkExtractor(allow=r"164-promos?page=[0-9]&sort=newest"),
            callback="parse_item",
            follow=True,
        )
    ]

    def parse_item(self, response):
        article = ArticleItem()
        yield article
        pass
