import re
from asgiref.sync import sync_to_async


class SaveItemPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        item.save()
        return item


class PreProcessPipeline:
    def process_item(self, item, spider):
        item["name"] = self._preprocess_value(item.get("name"))
        item["description"] = self._preprocess_value(item.get("description"))
        item["old_price"] = self._clean_price(item.get("old_price"))
        item["new_price"] = self._clean_price(item.get("new_price"))
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
    def _clean_price(price):
        if price:
            price = price.replace("\xa0", "").replace(",", ".")
            return float(price)
        return None
