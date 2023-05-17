from django.apps import AppConfig


class RecipesConfig(AppConfig):
    name = 'recipes'
    verbose_name = "Recipes, Comments, Likes"

    def ready(self):
        import recipes.signals