from django import template
from backend.models import Like

register = template.Library()


@register.filter
def has_liked(user, item):
    if user.is_authenticated:
        try:
            Like.objects.get(user=user, item=item)
            return True
        except Like.DoesNotExist:
            return False
    return False
