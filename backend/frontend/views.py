from django.shortcuts import render
from backend.models import Article

# Create your views here.
def home(request):
    articles = Article.objects.all()
    return render(request, 'frontend/home.html', {"articles": articles})