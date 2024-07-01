from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from backend.models import Category, Item, Like, Shop

NUMBER_OF_ITEMS_IN_PAGE = 8
NUMBER_OF_TOP_ITEMS = 24


def _generate_pages(ordered_items, page_number):
    paginator = Paginator(ordered_items, per_page=NUMBER_OF_ITEMS_IN_PAGE)
    items_in_page = paginator.get_page(page_number)
    items_in_page.adjusted_elided_pages = paginator.get_elided_page_range(
        page_number, on_each_side=2, on_ends=2
    )
    return items_in_page


def home(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "clear":
            post = request.POST.copy()
            post["shop"] = []
            request.POST = post
            request.session["shops"] = []
        else:
            request.session["shops"] = request.POST.getlist("shop")
        base_url = reverse("home")
        query_params = request.GET.copy()
        query_params["page"] = 1
        query_string = query_params.urlencode()
        url = f"{base_url}?{query_string}"
        return HttpResponseRedirect(url)

    shops_filter = request.session.get("shops", [])

    searched_item = request.GET.get("search")
    page_number = request.GET.get("page") or 1

    category = request.GET.get("category")
    sub_category = request.GET.get("sub_category")

    if category:
        request.session["shops"] = []

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

    sorted_items = items.order_by("-percentage", "-started_at")
    sub_categories = None

    if searched_item:
        display_items = sorted_items.filter(title__icontains=searched_item)
    elif category:
        display_items = sorted_items.filter(category__parent__name=category)
        sub_categories = Category.objects.filter(
            parent__name=category, items__isnull=False
        ).distinct()
        if sub_category:
            display_items = sorted_items.filter(category__name=sub_category)
    elif shops_filter:
        display_items = sorted_items.filter(provider__name__in=shops_filter)
    else:
        display_items = sorted_items

    items_in_page = _generate_pages(display_items, page_number)

    main_categories = Category.objects.filter(
        parent=None, sub_categories__items__isnull=False
    ).distinct()
    shops = Shop.objects.all()

    return render(
        request,
        "frontend/home.html",
        {
            "items": items_in_page,
            "searched_item": searched_item,
            "categories": main_categories,
            "selected_category": category,
            "sub_categories": sub_categories,
            "selected_sub_category": sub_category,
            "shops": shops,
            "shops_filtered": shops_filter,
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
