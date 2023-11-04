from django import template

register = template.Library()


@register.simple_tag
def is_liked(item, user):
    pass
