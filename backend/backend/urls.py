from django.contrib import admin
from django.urls import path
from backend.api import promotions


urlpatterns = [path("api/", promotions.api.urls)]
