import re
import scrapy
from scraper.items import ArticleItem

from backend.models import Item


category_mapping = {
    "accessory": [
        "Boucles d'oreilles",
        "Bagues Femme",
        "Montre Homme",
        "BABY-G ",
        "Montre Femme",
        "Casio",
        "Montre Enfant",
        "Bracelets Guess",
        "CASIO",
        "G-SHOCK",
        "Raymond Daniel",
        "Colliers Enzo Collection",
        "Colliers Guess",
        "Bracelets Enzo Collection",
        "Raymond Daniel ",
        "Edifice",
        "Portefeuilles BHPC",
        "Ceinture en Cuir",
        "Ceinture En Cuir",
        "Ceinture en cuir",
        "Ceinture en acier",
        "Ceinture En Acier",
        "Ceinture en Acier ",
        "Sac a Main ",
        "Portefeuilles Us Polo Assn",
        "Dream",
        "Beverly Hills Polo Club",
        "Pierre Cardin",
        "Lee Cooper",
        "Enzo Collection",
        "Enzo Collection ",
        "ENZO COLLECTION",
        "Accueil",
        "Slazenger",
    ],
    "electronics": ["SMARTWATCH", "ENZO DIGITAL"],
}


class CitywatchSpider(scrapy.Spider):
    name = "Citywatch"
    allowed_domains = ["citywatch.com.tn"]

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
    start_urls = ["https://citywatch.com.tn/promotions?from-xhr"]

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
        next_page_url = f"https://citywatch.com.tn/promotions?page={next_page}&from-xhr"  # noqa: E501
        yield scrapy.Request(
            url=next_page_url, callback=self.parse, meta={"page": next_page}
        )
