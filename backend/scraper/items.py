from scrapy_djangoitem import DjangoItem

from backend.models import Item


class ArticleItem(DjangoItem):
    django_model = Item
