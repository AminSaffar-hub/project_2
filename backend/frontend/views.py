from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from backend.models import Item, ItemRating

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


@require_POST
@csrf_exempt
def rate_item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        is_like = request.POST.get("like") == "true"
        user = request.user

        # Check if the user has already voted
        existing_vote = ItemRating.objects.filter(item=item, user=user).first()
        if existing_vote:
            if existing_vote.user_sentiment == is_like:
                existing_vote.user_sentiment = None
            else:
                existing_vote.user_sentiment = is_like
            existing_vote.save()
        else:
            ItemRating.objects.create(item=item, user=user, user_sentiment=is_like)

        # Calculate the updated vote counts
        like_count = item.rating.filter(user_sentiment=True).count()
        dislike_count = item.rating.filter(user_sentiment=False).count()
        return JsonResponse(
            {
                "like_count": like_count,
                "dislike_count": dislike_count,
            }
        )

    except Item.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)
