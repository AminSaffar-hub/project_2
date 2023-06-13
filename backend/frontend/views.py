from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import DetailView
from backend.models import Item


NUMBER_OF_ITEMS_IN_PAGE = 8


# Create your views here.
def home(request):
    searched_item = request.GET.get("search")
    page_number = request.GET.get("page") or 1
    if searched_item:
        items = Item.objects.filter(title__icontains=searched_item)
    else:
        items = Item.objects.all()

    paginator = Paginator(items.order_by("title"), per_page=NUMBER_OF_ITEMS_IN_PAGE)
    items_in_page = paginator.get_page(page_number)
    items_in_page.adjusted_elided_pages = paginator.get_elided_page_range(
        page_number, on_each_side=2, on_ends=2
    )

    return render(
        request,
        "frontend/home.html",
        {"items": items_in_page, "searched_item": searched_item},
    )


class ProductDetails(DetailView):
    model = Item
    template_name = "frontend/item_details.html"
