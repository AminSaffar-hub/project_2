from django import template

register = template.Library()


@register.simple_tag
def count_likes(item):
    return item.rating.filter(user_sentiment=True).count()


@register.simple_tag
def count_dislikes(item):
    return item.rating.filter(user_sentiment=False).count()
