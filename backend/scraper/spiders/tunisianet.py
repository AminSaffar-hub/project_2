import re

import scrapy
from scraper.items import ArticleItem

from backend.models import Item

category_mapping = {
    "electronics": [
        "webcam",
        "cafetiere-tunisie",
        "disques-ssd",
        "seche-cheveux-tunisie",
        "smartwatch",
        "pc-tout-en-un",
        "videoprojecteurs",
        "serveur-stockage-tunisie",
        "switch-routeurs-point-d-acces",
        "imprimante-en-tunisie",
        "tablette",
        "imprimante-et-multifonction-laser",
        "appareil-de-cuisson-convivial",
        "imprimante-professionnelle",
        "hachoir-tunisie-a-viande",
        "robot-multifonction-tunisie",
        "imprimante-point-de-vente",
        "appareils-photos-numerique",
        "lave-vaisselle-tunisie",
        "ecran-pc-tunisie",
        "pc-portable-tunisie",
        "informatique",
        "chauffage-tunisie",
        "pc-portable-gamer",
        "casque-ecouteurs",
        "smartphone-tunisie",
        "onduleur",
        "telephonie-tablette",
        "refrigerateur-tunisie",
        "scooter-electriques",
        "photocopieurs-a4-a3",
        "mixeur-plongeant-tunisie",
        "vente-tv-samsung-led-tunisie",
        "four-electrique-tunisie-micro-onde",
        "aspirateur-tunisie-vapeur",
        "montre-homme-femme-tunisie",
        "manettes-de-jeux",
        "imprimante-a-reservoir-integre",
        "pc-de-bureau",
    ]
}


class TunisiaNetSpider(scrapy.Spider):
    name = "Tunisia_Net"
    allowed_domains = ["tunisianet.com.tn"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
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

    start_urls = ["https://www.tunisianet.com.tn/promotions?from-xhr"]

    def parse(self, response):
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
                item["provider"] = "Tunisianet"
                item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
                item["online_payment"] = True
                reverse_mapping = {
                    value: key
                    for key, values in category_mapping.items()
                    for value in values
                }
                category_name = product["url"].split("/")[3]
                associated_key = reverse_mapping.get(category_name)
                if associated_key:
                    item["category"] = associated_key
                else:
                    item["category"] = "other"
                yield item
        current_page = response.meta.get("page", 1)
        self.logger.info(f"Currently on page: {current_page}")
        next_page = current_page + 1
        next_page_url = (
            f"https://www.tunisianet.com.tn/promotions?page={next_page}&from-xhr"
        )
        yield scrapy.Request(
            url=next_page_url, callback=self.parse, meta={"page": next_page}
        )
