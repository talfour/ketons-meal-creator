# from rest_framework.serializers import (
#     HyperlinkedIdentityField,
#     ModelSerializer,
#     SerializerMethodField
# )

# from recipes.models import Recipe

# class RecipeSerializer(ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = [
#             'id',
#             'author',
#             'slug',
#             'title',
#             'content',
#             'ingredients',
#             'prepare_time',
#             'images',
#             'liked',
#             'created',
#         ]