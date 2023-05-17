from django.urls import path

from .views import FoodDetailView, FoodListView, FoodCreateView

app_name = 'food'
urlpatterns = [
    path('', FoodListView.as_view(),name="food-list"),
    path("create/", FoodCreateView.as_view(), name="food-create"),
    path("<slug>", FoodDetailView.as_view(), name="food-details"),
]
