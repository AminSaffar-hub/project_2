from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView

from backend.models import Item

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

    if searched_item:
        items = Item.objects.filter(title__icontains=searched_item)
    elif category:
        items = Item.objects.filter(category=category)
    else:
        items = Item.objects.all()

    items_in_page = _generate_pages(items.order_by("title"), page_number)

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


def top_promos(request):
    page_number = request.GET.get("page") or 1
    ordered_items = sorted(
        Item.objects.all(), key=lambda t: t.sale_percentage, reverse=True
    )[:NUMBER_OF_TOP_ITEMS]
    items_in_page = _generate_pages(ordered_items, page_number)

    return render(
        request,
        "frontend/home.html",
        {"items": items_in_page, "searched_item": None},
    )


class ProductDetails(DetailView):
    model = Item
    template_name = "frontend/item_details.html"
