import re

import scrapy
from scrapy.http import Request

from backend.models import Item
from scraper.items import ArticleItem


class ZaraSpider(scrapy.Spider):
    name = "zara"
    allowed_domains = ["www.zara.com"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "*/*",
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
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            ),
        }
    }

    start_urls = [
        "https://www.zara.com/tn/fr/category/2291858/products?ajax=true",
        "https://www.zara.com/tn/fr/category/2299309/products?ajax=true",
        "https://www.zara.com/tn/fr/category/2137886/products?ajax=true",
    ]

    def parse(self, response):
        pattern = r'],"name":"(.*?)","description":".*?","price":(\d+),"oldPrice":(\d+),"displayDiscountPercentage":(\d+)'  # noqa: E501
        matches = re.findall(pattern, response.text)
        pattern_ids = r'"id":(\d+),"reference"'
        ids = re.findall(pattern_ids, response.text)
        pattern_reference = r'"id":\d+,"reference":"(\d+)-\w+"'
        references = re.findall(pattern_reference, response.text)
        pattern_keyword = r'"keyword":"([^"]+)"'
        keywords = re.findall(pattern_keyword, response.text)
        for match, reference, keyword, id in zip(matches, references, keywords, ids):
            name, price, old_price, discount_percentage = match
            item_url = (
                "https://www.zara.com/tn/fr/"
                + keyword
                + "-p"
                + reference
                + ".html?v1="
                + id
                + "&v2=2291858&ajax=true"
            )
            yield Request(
                url=item_url,
                callback=self.parse_product,
                meta={
                    "name": name,
                    "price": price,
                    "old_price": old_price,
                    "reference": reference,
                    "keyword": keyword,
                    "id": id,
                },
            )

    def parse_product(self, response):
        name = response.meta["name"]
        price = response.meta["price"]
        old_price = response.meta["old_price"]
        reference = response.meta["reference"]
        keyword = response.meta["keyword"]
        description_pattern = r',"description":"([^"]*)"'
        description_pre = (
            re.search(description_pattern, response.text).group(1)
            if re.search(description_pattern, response.text)
            else ""
        )
        description = description_pre.replace("\\n", " ").strip()
        image_pattern = r',"path":"(/[^"]+)","name":"([^"]+)","width":\d+,"height":\d+,"timestamp":"(\d+)"'  # noqa: E501
        image = re.search(image_pattern, response.text)
        item = ArticleItem()
        item["title"] = name
        item["discounted_price"] = int(price) / 100
        item["price"] = int(old_price) / 100
        item["link_to_post"] = (
            "https://www.zara.com/tn/fr/" + keyword + "-p" + reference + ".html"
        )
        item["link_to_image"] = (
            "https://static.zara.net/photos//"
            + image.group(1)
            + "/w/750/"
            + image.group(2)
            + ".jpg?ts="
            + image.group(3)
        )
        item["category"] = "clothes"
        item["description"] = description
        item["provider"] = "Zara"
        item["delivery"] = Item.DeliveryOptions.WITH_CONDITONS
        item["online_payment"] = True
        yield item
