import scrapy
from scraper.items import ArticleItem
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from backend.models import Item

category_mapping = {
    "cosmetics": [
        "ecrans-solaires-invisible",
        "eau-micellaire",
        "savon-nettoyant",
        "huile-solaire-et-bronzante",
        "soins-eclaircissantsvisage",
        "pince-a-epiler",
        "serum-hydratant-ampoule",
        "parfums",
        "soin-liftant-visage",
        "gloss-a-levres",
        "les-mascaras",
        "roll-on-femme",
        "hydratants-peaux-normales-a-mixtes",
        "proteine",
        "gel-douche",
        "lait-hydratant",
        "highlighter",
        "outils-de-manucure",
        "creme-premieres-rides",
        "soins-ongles",
        "seche-ongles-",
        "masques",
        "creme-anti-age-peau-mixte",
        "biberon",
        "crayons-a-levres",
        "hydratants-peaux-atopiques",
        "le-visage",
        "defenses-immunitaires",
        "soins-apaisants",
        "cremes-matifiantes-peaux-mixtes-a-grasses",
        "poudres-maquillage",
        "anti-vergetures",
        "-hydratants-peaux-sensibles-",
        "sexualite",
        "cheveux-solaire",
        "deodorant-femme",
        "huile-corporelle",
        "creme-cicatrisante--",
        "huile-lavante",
        "ecrans-solaires-teintes",
        "correcteur-et-anti-cernes",
        "brume-de-corps",
        "creme-apaisante-peau-sensible",
        "dentifrice",
        "creme-et-lait-apres-soleil-cosmetique",
        "bain-de-bouche-",
        "pinceaux",
        "fixateur-cheveux",
        "soins-peaux-a-imperfections",
        "apres-shampoing",
        "soins-des-pieds-jambes",
        "eyeliners",
        "vernis-a-ongles",
        "bons-plans_",
        "keratine",
        "eaux-de-parfum-femme",
        "creme-baume",
        "shampoing-cheveux-secs",
        "gel-intime",
        "soins-peau-grasse-mixte-et-acne",
        "gel-nettoyant-visage",
        "croutes-de-lait",
        "glucometres",
        "hydratation-visage-et-corps",
        "-creme-de-nuit-hydratant-visage",
        "soins-anti-taches-et---depigmentants",
        "soins-des-mains",
        "complements-cheveux",
        "appareil-soin-de-visage-",
        "rouges-a-levres",
        "crayon-yeux-khol",
        "brosse-peigne",
        "tire-lait",
        "fonds-de-teint",
        "savon",
        "roll-on-homme",
        "desinfectants-desodorisants",
        "special-ete-2022",
        "rides-marquees-perte-de-fermete",
        "bons-plans-",
        "ponceuse",
        "creme-de-jour-hydratant-visage",
        "fixateurs-de-maquillage",
        "palette-maquillage-yeux",
        "eponge-",
        "soin-contour-des-yeux",
        "accessoiresbb",
        "brosse-nettoyante",
        "-atomiseur",
        "hydratants-peaux-seches",
        "creme-anti-age-peau-seche",
        "complement-alimentaire",
        "corps-solaire",
        "lait-et-mousse-demaquillantes",
        "shampoing-cheveux-fins-cassants",
        "poudres-bronzantes",
        "vernis-fixateurs",
        "produit-solaires-tunisie",
        "serums-ampoules-capillaires",
        "trousseaux-et-cadeaux",
        "fards-a-joues",
        "masques-hydratants-pour-le-visage",
        "spray-solaire",
        "masques-visage-et-gommage",
        "soins-anti-rougeurs-et-peau-sensible",
        "nettoyer",
        "deodorant-homme",
        "primer",
        "toilette-bain-de-bebe",
        "le-collagene",
        "cheveux-soins-cosmetique",
        "soin-des-levres",
        "sale-promo",
        "contouring",
        "spray-coiffant",
        "deodorants-et-anti-transpirants",
        "gel-sourcils",
        "ombres-a-paupieres",
        "demaquillants-et-nettoyants-visage",
        "serum-anti-age-visage",
        "ciseaux",
        "cires-a-epiler",
    ]
}


class CosmetiqueSpider(CrawlSpider):
    name = "cosmetique"
    allowed_domains = ["cosmetique.tn"]
    start_urls = ["https://cosmetique.tn/promotions?page=1"]
    rules = [
        Rule(
            LinkExtractor(allow=r"promotions\?page=\d+"),
            callback="fetch_items",
            follow=True,
        )
    ]
    page_number = 1

    def parse_item(self, response):
        item = ArticleItem()
        item["title"] = response.css(".product-title::text").getall()
        item["discounted_price"] = response.css("span.price::text").get()
        item["price"] = response.css(".regular-price::text").get()
        item["link_to_post"] = response.url
        item["link_to_image"] = response.css(".js-qv-product-cover::attr(src)").get()
        item["category"] = "cosmetics"
        item["description"] = response.css(
            '[id^="product-description-"] *::text'
        ).extract()
        item["provider"] = "Cosmetique"
        item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
        item["online_payment"] = True
        yield item

    def fetch_items(self, response):
        if response.status == 404:
            raise CloseSpider("No more pages, quitting !!")

        items = response.css(
            "article.product-miniature div div h3 a::attr(href)"
        ).getall()

        if not len(items):
            raise CloseSpider(f"Empty page {self.page_number}, quitting !!")

        for article_url in items:
            yield scrapy.Request(
                url=response.urljoin(article_url),
                callback=self.parse_item,
            )
        self.page_number += 1
        next_page = f"https://cosmetique.tn/promotions?page={self.page_number}"
        yield response.follow(next_page, callback=self.fetch_items)
