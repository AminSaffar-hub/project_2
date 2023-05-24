from django.shortcuts import render
from django.core.paginator import Paginator
from backend.models import Article

# Create your views here.
def home(request, page=1):
    search_post = request.GET.get('search')
    if search_post:
        articles = Article.objects.filter(name__icontains=search_post).order_by("name")
    else:
        articles = Article.objects.all().order_by("name")

    paginator = Paginator(articles, per_page=8)
    articles_in_page = paginator.get_page(page)
    articles_in_page.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=2, on_ends=2)

    return render(request, 'frontend/home.html', {"articles": articles_in_page, "search_post": search_post})