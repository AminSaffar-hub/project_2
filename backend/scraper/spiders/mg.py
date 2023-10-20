import scrapy
from scraper.items import ArticleItem

from backend.models import Item


class MgSpider(scrapy.Spider):
    name = "Magasin_general"
    allowed_domains = ["https://mg.tn/"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "YOUR_COOKIE_HERE",
            "Host": "mg.tn",
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

    start_urls = ["https://mg.tn/61-promotion?page=1&from-xhr"]

    def start_requests(self):
        urls = [
            ("https://mg.tn/61-promotion?page=1&from-xhr", "food"),
            ("https://mg.tn/64-promotion?page=1&from-xhr", "self-care"),
            ("https://mg.tn/67-promotion?page=1&from-xhr", "appliances"),
            ("https://mg.tn/61-promotion?page=2&from-xhr", "food"),
            ("https://mg.tn/64-promotion?page=2&from-xhr", "self-care"),
            ("https://mg.tn/67-promotion?page=2&from-xhr", "appliances"),
            ("https://mg.tn/61-promotion?page=3&from-xhr", "food"),
            ("https://mg.tn/64-promotion?page=3&from-xhr", "self-care"),
            ("https://mg.tn/67-promotion?page=3&from-xhr", "appliances"),
        ]

        for url, category in urls:
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"category": category}
            )

    def parse(self, response):
        data = response.json()
        category = response.meta["category"]

        for product in data["products"]:
            item = ArticleItem()
            item["title"] = product["name"]
            item["discounted_price"] = float(product["price_amount"])
            item["price"] = float(product["regular_price_amount"])
            item["link_to_post"] = product["url"]
            item["link_to_image"] = product["cover"]["large"]["url"]
            item["category"] = category
            item["description"] = (
                product["description_short"].replace("<br />", "").replace("</b>", "")
            )
            item["provider"] = "Magasin General"
            item["delivery"] = Item.DeliveryOptions.NOT_AVAILABLE
            item["online_payment"] = False
            yield item
