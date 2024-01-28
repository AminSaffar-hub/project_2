from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from backend.models import Item, Category, Shop, Like


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
    shop = request.GET.get("shop")

    items = Item.objects.annotate(
        percentage=ExpressionWrapper(
            100
            * (F("price") - F("discounted_price"))
            * F("provider__score")
            * F("category__score")
            / F("price"),
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
    elif shop:
        display_items = sorted_items.filter(provider__name=shop)
    else:
        display_items = sorted_items

    items_in_page = _generate_pages(display_items, page_number)

    categories = Category.objects.all()
    shops = Shop.objects.all()
    return render(
        request,
        "frontend/home.html",
        {
            "items": items_in_page,
            "searched_item": searched_item,
            "categories": categories,
            "category": category,
            "shops": shops,
            "shop": shop,
        },
    )


def footer_info(request):
    return render(request, "frontend/footer_info.html")


@require_POST
@csrf_exempt
def like_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    user = request.user

    like_exists = Like.objects.filter(item=item, user=user).exists()
    if like_exists:
        Like.objects.get(item=item, user=user).delete()
        return JsonResponse({"like": False})
    else:
        Like.objects.create(item=item, user=user)
        return JsonResponse({"like": True})


class ProductDetails(DetailView):
    model = Item
    template_name = "frontend/item_details.html"


def error_404_view(request, exception):
    return render(request, "frontend/404.html")
