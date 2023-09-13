from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField
from django.shortcuts import render
from django.views.generic import DetailView

from backend.models import Item

NUMBER_OF_ITEMS_IN_PAGE = 8
NUMBER_OF_TOP_ITEMS = 24

SALE_PERCENTAGE_WEIGHT = 0.8
PRICE_WEIGHT = 0.2


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
    )

    items = items.annotate(
        weighted_score=ExpressionWrapper(
            (SALE_PERCENTAGE_WEIGHT * F("percentage")) + PRICE_WEIGHT * F("price"),
            output_field=FloatField(),
        )
    )

    if searched_item:
        items = items.filter(title__icontains=searched_item)
    elif category:
        items = items.filter(category=category)
    else:
        items = items.all()

    current_promotions = items.filter(
        price__isnull=False,
        discounted_price__isnull=False,
    )
    sorted_items = current_promotions.order_by("-weighted_score")

    items_in_page = _generate_pages(sorted_items, page_number)

    categories = Item.ItemCategories.choices
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
