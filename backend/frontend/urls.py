from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>", views.ProductDetails.as_view(), name="product_details"),
    path("top-promos", views.top_promos, name="top-promos")
]
