import json
import re

import scrapy

from backend.models import Item
from scraper.items import ArticleItem

category_mapping = {
    "electronics": [
        "Sécurité ",
        "Univers Telephonie",
        "Smartphones",
        "Tablette",
        "Univers Informatique",
        "Smartwatch Tunisie",
        "Box android",
        "TV",
        "Tv |Audio , Vidéo et Photo",
        "Univers Maison",
    ],
    "appliances": ["GAZ Plaque", "Robot De Cuisine", "Cafetière", "Lave Vaisselle "],
    "other": [
        "Frontale",
        "Accessoires Téléphonies ",
        "Ventes Flash et Meilleur Promo",
        "Accueil",
    ],
}


class TunisiatechSpider(scrapy.Spider):
    name = "Tunisiatech"
    allowed_domains = ["tunisiatech.tn"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",  # noqa: E501
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "ROBOTSTXT_OBEY": False,
            "Authorization": "Bearer null",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DNT": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User": "anonymous",
        },
    }

    start_urls = ["https://tunisiatech.tn/177-ventes-flash-et-meilleur-promo?from-xhr"]

    def parse(self, response):
        data = response.json()
        with open("data.json", "w") as f:
            json.dump(data, f)
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
                reverse_mapping = {
                    value: key
                    for key, values in category_mapping.items()
                    for value in values
                }
                category_name = product["category_name"]
                associated_key = reverse_mapping.get(category_name)
                if associated_key:
                    item["category"] = associated_key
                else:
                    item["category"] = "other"
                yield item
        current_page = response.meta.get("page", 1)
        self.logger.info(f"Currently on page: {current_page}")
        next_page = current_page + 1
        next_page_url = f"https://tunisiatech.tn/177-ventes-flash-et-meilleur-promo?page={next_page}&from-xhr"  # noqa: E501
        yield scrapy.Request(
            url=next_page_url, callback=self.parse, meta={"page": next_page}
        )
