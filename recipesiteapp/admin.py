from django.contrib import admin
from .models import Recipe, Category, RecipesCategories

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(RecipesCategories)
