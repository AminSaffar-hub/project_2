import re
import scrapy
from scraper.items import ArticleItem
from backend.models import Item
import requests

class PeakSpider(scrapy.Spider):
    name = "Peak"
    allowed_domains = ["peaksports.tn"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",  # noqa: E501
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",  # noqa: E501
            "X-Requested-With": "XMLHttpRequest",
        },
    }
    start_urls = ["https://www.peaksports.tn/promotions?page=2&from-xhr="]

    def parse(self, response):
        response_json = requests.get(
            "https://www.peaksports.tn/promotions?page=2&from-xhr="
        )

        # only proceed if I have a 200 response which is saved in status_code
        if response_json.status_code == 200:
            response = response_json.json()
        print(response)
        data = response.json()

        if not data.get("products"):
            self.logger.info("No products found. Stopping spider.")
            return  # Stop if there's no product
        for product in data["products"]:
            if product["active"] == "1":
                item = ArticleItem()
                item["title"] = product["name"]
                item["discounted_price"] = float(product["price_amount"])
                item["price"] = float(product["regular_price_amount"])
                item["link_to_post"] = product["url"]
                item["link_to_image"] = product["cover"]["large"]["url"]
                item["description"] = re.sub(r"<.*?>", "", product["description_short"])
                item["provider"] = self.name
                item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
                item["online_payment"] = True
                yield item
        current_page = response.meta.get("page", 1)
        self.logger.info(f"Currently on page: {current_page}")
        next_page = current_page + 1
        next_page_url = f"https://www.peaksports.tn/promotions?page={next_page}&from-xhr"  # noqa: E501
        yield scrapy.Request(
            url=next_page_url, callback=self.parse, meta={"page": next_page}
        )

    def close(self):
        print(set(self.l))
