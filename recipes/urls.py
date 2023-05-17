from django.urls import path
# from .views import create_recipe_view
from .views import RecipeDeleteView, RecipeUpdateView, RecipeListView, RecipeDetailView, RecipeCreateView, UserRecipeBookListView, add_recipe_to_book, check_recipe, get_recipe, like_unlike_recipe, load_weight
app_name = 'recipes'

urlpatterns = [

    path("", RecipeListView.as_view(), name="main-recipe-view"),
    path("get/recipe", get_recipe, name="get_recipe"),
    path("get/load_weights", load_weight, name="load_weights"),
    path("user_recipes/", UserRecipeBookListView.as_view(), name="user-recipe-view"),
    path("get/check_recipe", check_recipe, name="check_recipe"),
    path('new/', RecipeCreateView.as_view(), name="create-recipe"),
    path('recipe_liked/', like_unlike_recipe, name="like-recipe-view"),
    path('add_to_book/', add_recipe_to_book, name="add-to-book"),
    path('<slug>/', RecipeDetailView.as_view(), name="recipe-detail-view"),
    path('<pk>/delete/', RecipeDeleteView.as_view(), name="recipe-delete"),
    path('<pk>/update/', RecipeUpdateView.as_view(), name="recipe-update"),

]
