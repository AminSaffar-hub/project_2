import scrapy

from backend.models import Item
from scraper.items import ArticleItem


class chillandlit(scrapy.Spider):
    name = "Chillandlit"
    allowed_domains = ["chillandlit.tn"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "YOUR_COOKIE_HERE",
            "Host": "chillandlit.tn",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",  # noqa: E501
            "X-Requested-With": "XMLHttpRequest",
        }
    }

    start_urls = ["https://chillandlit.tn/222-promos?page=1&from-xhr"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.json()
        if not data.get("products"):
            self.logger.info("No products found. Stopping spider.")
            return

        for product in data["products"]:
            item = ArticleItem()
            item["title"] = product["name"]
            item["discounted_price"] = float(product["price_amount"])
            item["price"] = float(product["regular_price_amount"])
            item["link_to_post"] = product["url"]
            item["link_to_image"] = product["cover"]["large"]["url"]
            item["description"] = (
                product["description_short"].replace("<br />", "").replace("</b>", "")
            )
            item["provider"] = self.name
            item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
            item["online_payment"] = False
            item["category"] = "clothes"
            yield item
        current_page = response.meta.get("page", 1)
        self.logger.info(f"Currently on page: {current_page}")
        next_page = current_page + 1
        next_page_url = f"https://chillandlit.tn/222-promos?page={next_page}&from-xhr"
        yield scrapy.Request(
            url=next_page_url, callback=self.parse, meta={"page": next_page}
        )
