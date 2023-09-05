from django import template

register = template.Library()


@register.simple_tag
def rating_count(item):
    user_likes = item.rating.filter(user_sentiment=True).count()
    user_dislikes = item.rating.filter(user_sentiment=False).count()
    return user_likes - user_dislikes
