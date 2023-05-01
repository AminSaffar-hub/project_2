from datetime import datetime
from ninja import Field, NinjaAPI, Schema
from backend import models
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)


class ArticleIn(Schema):
    name: str = Field(default=None)
    original_price: float = Field(default=None)
    reduced_price: float = Field(default=None)
    location: str = Field(default=None)
    image: str = Field(default=None)
    sector: str = Field(default=None)
    ended_at: datetime = Field(default=None)


class Message(Schema):
    message: str


@api.post("/promotions", response=Message)
def add_article(request, body: ArticleIn):
    """
    posts a new article to the database
    """
    models.Article.objects.create_from_body(**body.dict())
    return {"message": "article added successfully"}
