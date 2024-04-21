import re

import scrapy
from scraper.items import ArticleItem

from backend.models import Item


class TdiscountSpider(scrapy.Spider):
    name = "tdiscount"
    allowed_domains = ["tdiscount.tn"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.,en;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',  # noqa: E501
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",  # noqa: E501
            "X-Requested-With": "XMLHttpRequest",
        }
    }

    start_urls = ["https://tdiscount.tn/promotions?page=1&from-xhr"]

    def parse(self, response):
        content_type = response.headers.get("Content-Type", b"").decode("utf-8").lower()
        if "application/json" not in content_type:
            self.logger.warning(f"Unexpected Content-Type: {content_type}")
            return
        data = response.json()

        if not data.get("products"):
            self.logger.info("No products found. Stopping spider.")
            return

        for product in data["products"]:
            if product["active"] == "1":
                item = ArticleItem()
                item["title"] = product["name"]
                item["discounted_price"] = float(product["price_amount"])
                item["price"] = float(product["regular_price_amount"])
                item["link_to_post"] = product["url"]
                item["link_to_image"] = product["cover"]["large"]["url"]
                item["description"] = re.sub(r"<.*?>", "", product["description_short"])
                item["provider"] = "Tdiscount"
                item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
                item["online_payment"] = True
                yield item

        current_page = response.meta.get("page", 1)
        self.logger.info(f"Currently on page: {current_page}")
        next_page = current_page + 1
        next_page_url = f"https://tdiscount.tn/promotions?page={next_page}&from-xhr"
        yield scrapy.Request(
            url=next_page_url, callback=self.parse, meta={"page": next_page}
        )
