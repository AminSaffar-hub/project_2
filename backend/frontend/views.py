from django.shortcuts import render
from backend.models import Article

# Create your views here.
def home(request):
    search_post = request.GET.get('search')
    if search_post:
        articles = Article.objects.filter(name__icontains=search_post)
    else:
        articles = Article.objects.all()
    return render(request, 'frontend/home.html', {"articles": articles})