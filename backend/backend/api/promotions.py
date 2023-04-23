from datetime import datetime
from ninja import NinjaAPI, Schema
from backend import models
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)


class ArticleIn(Schema):
    name: str
    original_price: float
    reduced_price: float
    location: str
    image: str
    sector: str
    ended_at: datetime


class Message(Schema):
    message: str


@api.post("/promotion", response=Message)
def add_article(request, body: ArticleIn):
    """
    posts a new article to the database
    """
    models.Article.objects.create_from_body(**body.dict())
    return {"message": "article added successfully"}
