import re

import scrapy
from scraper.items import ArticleItem

from backend.models import Item

category_mapping = {
    "cosmetics": [
        "démaquillants",
        "beauté-et-santé",
        "maquillage-des-yeux",
        "soin-des-ongles",
        "maquillage-du-teint",
        "shampooings",
        "maquillage-des-lèvres",
        "eaux-de-toilette-et-eaux-de-cologne",
        "lotions-capillaires-fixateurs",
        "accessoires-cheveux",
        "epilation-et-rasage-femme",
    ],
    "self-care": [
        "hygiène-dentaire",
        "mouchoirs",
        "déodorants",
        "shampooings-et-soin-du-bébé",
        "après-shampooings",
        "papiers-hygiéniques",
        "couches-et-lingettes",
        "gels-douche-savons-et-gels-désinfectants",
        "hygiène-intime-et-périodique",
        "trousses-de-toilette-et-accessoires",
        "crèmes-et-laits-hydratants",
        "eau-de-javel",
        "cotons",
        "rasage-homme",
        "absorbant-essuyage-et-brosserie",
        "essuie-tout-et-serviettes-en-papier",
        "pour-vaisselles-mains",
    ],
    "food": [
        "colorations",
        "plats-cuisinés",
        "cornichonsolives-et-condiments",
        "huiles-vinaigrescondiments-et-sauces",
        "desserts-à-préparer",
        "volaille",
        "jus-de-fruit-lacte",
        "vinaigres-vinaigrettes-et-sauces-salades",
        "bœuf",
        "bonbons",
        "nectar-de-fruits",
        "céréales-et-barres-céréalières",
        "thons",
        "biscuits-secs",
        "fromages-à-tartiner",
        "epices",
        "pates",
        "boissons-gazeuses",
        "pur-jus-de-fruits",
        "harissa",
        "barres-biscuitées",
        "beurres-et-margarines",
        "crèmes-dessert",
        "huiles-d-olive",
        "frites",
        "viande-volaille",
        "biscottes",
        "pains-et-viennoiseries",
        "mayonnaise",
        "yaourts",
        "gaufrettes",
        "sucres",
        "chamia",
        "cafés-moulus",
        "tomates",
        "pâtes-fraiches",
        "poissons-et-crustacés",
        "lait",
        "pâtes-à-tartiner",
        "volaille-et-lapin",
        "rôtisserie-et-grillade",
        "gâteauxglaces-et-desserts",
        "huiles-végétales",
        "oeufs",
        "miels",
        "madeleines-et-cakes",
        "chips-et-pop-corn",
        "fromages-râpés-et-de-cuisson",
        "fromages-blancs",
        "legumes",
        "cola-et-boissons-gazeuses",
        "cafés-solubleschicorées",
        "moutarde-et-ketchup",
        "fromages-en-portions",
        "pâtes-à-tarte",
        "19182-boissons-énergétiques.html",
        "biscuits-apéritifs",
        "chocolat-en-poudre",
        "chocolats-fourrés",
        "confitures",
        "farines-et-semoules",
        "29885-boisson-énergitique.html",
        "produits-salés-apéritifs",
        "biscuits-à-la-crème",
        "tablettes-et-barres-de-chocolat",
    ],
    "appliances": [
        "art-de-la-table",
        "sacs-poubelles-et-autres-sacs",
        "quincaillerie",
        "outils-et-entretien-de-jardin",
        "cuisine-et-salle-de-bain",
        "liquides-et-poudres-machine",
        "vaisselles-en-carton-et-en-plastique",
        "bricolage",
        "paniers-corbeilles-et-éléments-de-rangements",
        "assouplissants-et-détachants",
        "nettoyants-divers",
        "sols-et-carrelages",
        "films-alimentaires-et-papier-cuisson",
        "savons-de-ménage-liquides-et-poudres-mains",
        "desodorisants",
        "petits-appareils-de-cuisine",
        "rangement-et-conservation",
        "aides-à-la-pâtisserie",
        "ustensiles-de-cuisine",
        "barquettes-et-papiers-aluminium",
    ],
    "electronics": ["chauffage-et-radiateur"],
    "other": [
        "librairie",
        "tous-les-produits",
        "jouets-enfant",
        "déco-cadeaux-et-articles-de-fête",
        "vélocyclisme-et-patinage",
    ],
    "pets": ["aliments-chiens", "aliments-chats", "accessoires-chats"],
}


class MonoprixSpider(scrapy.Spider):
    name = "monoprix"
    allowed_domains = ["monoprix.tn"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.,en;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",  # noqa: E501
            "X-Requested-With": "XMLHttpRequest",
        }
    }

    start_urls = ["https://courses.monoprix.tn/ennasr/promotions?page=1&from-xhr="]

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
                item["link_to_image"] = product["images"][0]["large"]["url"]
                item["description"] = re.sub(r"<.*?>", "", product["description_short"])
                item["provider"] = "Monoprix"
                item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
                item["online_payment"] = True
                category_name = product["url"].split("/")[4]
                reverse_mapping = {
                    value: key
                    for key, values in category_mapping.items()
                    for value in values
                }
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
            f"https://courses.monoprix.tn/ennasr/promotions?page={next_page}&from-xhr="
        )
        yield scrapy.Request(
            url=next_page_url, callback=self.parse, meta={"page": next_page}
        )
