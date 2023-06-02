import re


class SaveItemPipeline:
    def process_item(self, item, spider):
        item.save()
        return item


class PreProcessItemName:
    def process_item(self, item, spider):
        name = item.get("name")
        if isinstance(name, list):
            name = "".join(name)

        name = name.strip()
        name = re.sub(r"\s+", " ", name)
        name = re.sub(r"[^\w\s]", "", name)
        item["name"] = name
        return item


class PreProcessDescription:
    def process_item(self, item, spider):
        description = item.get("description")
        if isinstance(description, list):
            description = "".join(description)

        description = description.strip()
        description = re.sub(r"\s+", " ", description)
        description = re.sub(r"[^\w\s]", "", description)
        item["description"] = description
        return item


class PreProcessPrice:
    def process_item(self, item, spider):
        old_price = item.get("old_price")
        new_price = item.get("new_price")
        item["old_price"] = float(old_price.replace("\xa0", "").replace(",", "."))
        item["new_price"] = float(new_price.replace("\xa0", "").replace(",", "."))
        return item
