from django.contrib import admin
from .models import Recipe, RecipeIngredients, RecipeEvent
# Register your models here.
admin.site.register(Recipe)
admin.site.register(RecipeIngredients)
admin.site.register(RecipeEvent)
