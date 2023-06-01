from scrapy_djangoitem import DjangoItem
from backend.models import Article


class ArticleItem(DjangoItem):
    django_model = Article
