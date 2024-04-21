from django.conf.urls import handler404
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("frontend.urls")),
    path("", include("login.urls")),
]

handler404 = "frontend.views.error_404_view"  # noqa
