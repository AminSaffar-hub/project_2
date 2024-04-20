from django.contrib import admin

from backend.models import Category, Item, Like, Shop

# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Like)
