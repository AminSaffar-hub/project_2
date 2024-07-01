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


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    request = context["request"]
    query = request.GET.copy()

    query[field] = value

    if request.method == "POST" and request.POST.getlist("shop"):
        query["page"] = "1"

    return query.urlencode()
