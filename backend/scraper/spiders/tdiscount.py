import json
import scrapy
from scraper.items import ArticleItem

from backend.models import Item


class TdiscountSpider(scrapy.Spider):
    name = "tdiscount"
    allowed_domains = ["tdiscount.tn"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "authority": "tdiscount.tn",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "referer": "https://tdiscount.tn/promotions?page=1&from-xhr",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
        }
    }
    headers = {
        "authority": "tdiscount.tn",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://tdiscount.tn/promotions?page=1&from-xhr",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
    }

    def start_requests(self):
        urls = [
            "https://tdiscount.tn/promotions?page=1&from-xhr",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        content_type = response.headers.get("Content-Type", b"").decode("utf-8").lower()
        if "application/json" not in content_type:
            self.logger.warning(f"Unexpected Content-Type: {content_type}")
            return
        data = json.loads(response.text)

        if not data.get("products"):
            self.logger.info("No products found. Stopping spider.")
            return

        for product in data["products"]:
            if product["active"] == "1":
                item = ArticleItem()
                item["title"] = product.get("name")
                item["discounted_price"] = (
                    float(product.get("price_amount"))
                    if product.get("price_amount")
                    else "No price"
                )
                item["price"] = (
                    float(product.get("regular_price_amount"))
                    if product.get("regular_price_amount")
                    else ""
                )
                item["link_to_post"] = product.get("url", "")
                item["link_to_image"] = (
                    product.get("cover", {}).get("large", {}).get("url")
                )
                item["category"] = "appliances"
                item["description"] = product.get("description_short", "")
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
