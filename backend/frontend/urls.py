from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>", views.ProductDetails.as_view(), name="product_details"),
    path("footer_info/", views.footer_info, name="footer_info"),
    path("like_item/<int:item_id>/", views.like_item, name="rate"),
]
