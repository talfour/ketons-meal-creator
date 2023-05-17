from django.contrib import admin
from import_export import resources
# Register your models here.
from .models import Food, FoodWeight
from import_export.admin import ImportExportModelAdmin

@admin.register(Food)
# class FoodModelAdmin(admin.ModelAdmin):
    
#     list_display = ('name',)
#     search_fields = ['name']
#     ordering = ('-created',)

class FoodAdmin(ImportExportModelAdmin):
    pass

@admin.register(FoodWeight)
class FoodWeight(ImportExportModelAdmin):
    pass