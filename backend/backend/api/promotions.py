from datetime import datetime
from ninja import Field, NinjaAPI, Schema
from backend import models
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)


class ArticleIn(Schema):
    name: str = Field(default=None)
    old_price: float = Field(default=None)
    new_price: float = Field(default=None)
    url: str = Field(default=None)
    image_link: str = Field(default=None)
    type: str = Field(default=None)
    description: str = Field(default=None)


class Message(Schema):
    message: str


@api.post("/promotions", response=Message)
def add_article(request, body: ArticleIn):
    """
    posts a new article to the database
    """
    models.Article.objects.create_from_body(**body.dict())
    return {"message": "article added successfully"}
