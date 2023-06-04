from django.shortcuts import render
from django.core.paginator import Paginator
from backend.models import Article

NUMBER_OF_ARTICLES_IN_PAGE = 8


# Create your views here.
def home(request):
    searched_article = request.GET.get("search")
    page_number = request.GET.get("page") or 1
    if searched_article:
        articles = Article.objects.filter(name__icontains=searched_article)
    else:
        articles = Article.objects.all()

    paginator = Paginator(
        articles.order_by("name"), per_page=NUMBER_OF_ARTICLES_IN_PAGE
    )
    articles_in_page = paginator.get_page(page_number)
    articles_in_page.adjusted_elided_pages = paginator.get_elided_page_range(
        page_number, on_each_side=2, on_ends=2
    )

    return render(
        request,
        "frontend/home.html",
        {"articles": articles_in_page, "searched_article": searched_article},
    )
