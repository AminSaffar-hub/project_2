from itertools import zip_longest

from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField, Q
from django.shortcuts import render
from django.views.generic import DetailView

from backend.models import Item, Category

NUMBER_OF_ITEMS_IN_PAGE = 8
NUMBER_OF_TOP_ITEMS = 24


def _generate_pages(ordered_items, page_number):
    paginator = Paginator(ordered_items, per_page=NUMBER_OF_ITEMS_IN_PAGE)
    items_in_page = paginator.get_page(page_number)
    items_in_page.adjusted_elided_pages = paginator.get_elided_page_range(
        page_number, on_each_side=2, on_ends=2
    )
    return items_in_page


# Create your views here.
def home(request):
    searched_item = request.GET.get("search")
    page_number = request.GET.get("page") or 1
    category = request.GET.get("category")

    items = Item.objects.annotate(
        percentage=ExpressionWrapper(
            100 * (F("price") - F("discounted_price")) / F("price"),
            output_field=FloatField(),
        )
    ).filter(
        price__isnull=False,
        discounted_price__isnull=False,
    )

    sorted_items = items.order_by("-percentage")

    if searched_item:
        display_items = sorted_items.filter(title__icontains=searched_item)
    elif category:
        display_items = sorted_items.filter(category__name=category)
    else:
        categories = Category.objects.all()
        items_by_category = sorted_items.filter(Q(category__in=categories))
        display_items = []
        for items_in_category in zip_longest(
            *[items_by_category.filter(category=category) for category in categories]
        ):
            for item in items_in_category:
                if item is not None:
                    display_items.append(item)
        # display_items = sorted_items

    items_in_page = _generate_pages(display_items, page_number)

    categories = Category.objects.all()
    return render(
        request,
        "frontend/home.html",
        {
            "items": items_in_page,
            "searched_item": searched_item,
            "categories": categories,
            "category": category,
        },
    )


def footer_info(request):
    return render(request, "frontend/footer_info.html")


class ProductDetails(DetailView):
    model = Item
    template_name = "frontend/item_details.html"
