from itertools import zip_longest

from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, F, FloatField, Q
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
        display_items = sorted_items.filter(category=category)
    else:
        category_names = [category for category in Item.ItemCategories.values]
        items_by_category = sorted_items.filter(Q(category__in=category_names))
        display_items = []
        for items_in_category in zip_longest(
            *[
                items_by_category.filter(category=category)
                for category in category_names
            ]
        ):
            for item in items_in_category:
                if item is not None:
                    display_items.append(item)

    items_in_page = _generate_pages(display_items, page_number)

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


@require_POST
@csrf_exempt
def rate_item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        is_like = request.POST.get("like") == "true"
        user = request.user
        new_rating = False

        # Check if the user has already voted
        existing_vote = ItemRating.objects.filter(item=item, user=user).first()
        if existing_vote:
            if existing_vote.user_sentiment == is_like:
                existing_vote.user_sentiment = None
                new_rating = False
            else:
                existing_vote.user_sentiment = is_like
                new_rating = True
            existing_vote.save()
        else:
            new_rating = True
            ItemRating.objects.create(item=item, user=user, user_sentiment=is_like)

        # Calculate the updated vote counts
        like_count = item.rating.filter(user_sentiment=True).count()
        dislike_count = item.rating.filter(user_sentiment=False).count()
        return JsonResponse(
            {
                "new_vote": new_rating,
                "like_count": like_count,
                "dislike_count": dislike_count,
            }
        )

    except Item.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)
