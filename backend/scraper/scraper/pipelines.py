# useful for handling different item types with a single interface


class ScraperPipeline:
    def process_item(self, item, spider):
        item.save()
        return item
