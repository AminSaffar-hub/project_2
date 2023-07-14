import re
from asgiref.sync import sync_to_async


class SaveItemPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        item.save()
        return item


class PreProcessPipeline:
    def process_item(self, item, spider):
        item["title"] = self._preprocess_value(item.get("title"))
        item["description"] = self._preprocess_description(item.get("description"))
        item["price"] = self._clean_price(item.get("price"))
        item["discounted_price"] = self._clean_price(item.get("discounted_price"))
        return item

    @staticmethod
    def _preprocess_value(value):
        if isinstance(value, list):
            value = "".join(value)
        if value:
            value = value.strip()
            value = re.sub(r"\s+", " ", value)
            value = re.sub(r"[^\w\s]", "", value)
        return value

    @staticmethod
    def _preprocess_description(value):
        if isinstance(value, list):
            value = "\n".join(value)
        return value

    @staticmethod
    def _clean_price(price):
        if price:
            price = price.replace("\xa0", "").replace(",", ".")
            if price.find("TND") != -1:
                price = price.replace("TND", "")
            return float(price)
        return None
