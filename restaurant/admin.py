from django.contrib import admin
from .models import Category, Dish, Restaurant

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Restaurant)