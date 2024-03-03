import scrapy
from scraper.items import ArticleItem

from backend.models import Item


class fatale(scrapy.Spider):
    name = "fatale"
    allowed_domains = ["www.fatales.tn"]
    start_urls = ["https://www.fatales.tn/promotions?page=1"]

    def parse(self, response):
        articles = response.xpath('//div[@class="product-container"]//article')

        for article in articles:
            item = ArticleItem()

            item["title"] = article.xpath('.//a[@class="product-name"]//text()').get()
            item["discounted_price"] = float(
                article.xpath('.//span[@class="price product-price"]//text()').get()
            )
            item["price"] = float(
                article.xpath('.//span[@class="regular-price"]//text()').get()
            )
            item["link_to_post"] = article.xpath(
                './/a[@class="product-name"]/@href'
            ).get()
            item["link_to_image"] = article.xpath(
                './/a[@class="product_img_link"]//img/@src'
            ).get()
            item["category"] = article.xpath(
                './/span[@class="product-category"]//text()'
            ).get()
            item["description"] = ""
            item["provider"] = "fatale"
            item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
            item["online_payment"] = True

            yield item

        # Récupérer la page suivante
        # next_page = response.xpath('//a[@rel="next"]/@href').get()
        # if next_page:
        #   yield response.follow(next_page, self.parse)

        current_page = response.meta.get("page", 1)
        self.logger.info(f"Currently on page: {current_page}")
        next_page = current_page + 1
        next_page_url = f"https://tdiscount.tn/promotions?page={next_page}&from-xhr"
        yield scrapy.Request(
            url=next_page_url,
            callback=self.parse,
            meta={"page": next_page},
        )
