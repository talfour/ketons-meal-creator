from django.db import models
from food.models import Food, FoodWeight
from django.utils import timezone
from profiles.models import Profile
from django.core.validators import FileExtensionValidator
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from .utils import calculation_based_by_portions, calculation_based_by_quantity,  sum_up_nutritien, sum_up_nutritien_based_by_portions, sum_values_from_dictionary
from food.models import Food
from django_editorjs import EditorJsField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from profiles.utils import get_random_code

class Recipe(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="recipes")
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    title = models.CharField(max_length=100, db_index=True, verbose_name="Tytuł")
    content = EditorJsField(
        editorjs_config={
            'tools': {
                "Table": {
                    "disabled": True
                },
                "Quote":{
                    "disabled": True
                },
                "Raw":{
                    "disabled": True
                },
                "Embed":{
                    "disabled": True
                },
                "Delimiter":{
                    "disabled": True
                },
                "Attaches":{
                    "disabled": True
                },
                "Warning":{
                    "disabled": True
                },
                "Link":{
                    "disabled": True
                },
                "Checklist":{
                    "disabled": True
                }
            }
        }
    )
    ingredients = models.ManyToManyField(Food, through='RecipeIngredients')
    prepare_time = models.TimeField(verbose_name="Czas przygotowania")
    images = models.ImageField(upload_to='recipes', validators=[
                               FileExtensionValidator(['png', 'jpg', 'jpeg'])], default="recipes/default.png", verbose_name="Zdjęcie")
    liked = models.ManyToManyField(
        Profile, blank=True, related_name='likes')
    saved = models.ManyToManyField(
        Profile, blank=True, related_name="saves", db_index=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(verbose_name="Tagi", help_text="Tagi należy odzielić od siebie przecinkiem")
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    published = models.BooleanField(default=False, verbose_name="Czy chcesz publikować post?")
    portions = models.PositiveIntegerField(default=1, verbose_name="Ilość porcji")

    @property
    def formatted_markdown(self):
        return markdownify(self.content)

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if not self.slug:
            self.created = timezone.now()
            to_slug = slugify(str(self.author.user.username + " " +
                                    self.title + " " + self.created.strftime('%d-%m-%Y')))
            ex = Recipe.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Recipe.objects.filter(slug=to_slug).exists()
        self.slug = to_slug

        if self.images:
            self.images = self.compressImage(self.images)
        # else:
        #     self.created = timezone.now()
        #     to_slug = str(self.title + self.created.strftime('%d-%m-%Y'))
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('recipes:recipe-detail-view', kwargs={"slug": self.slug})

    def num_likes(self):
        return self.liked.all().count()

    def get_nutrition_info(self):
        food_list = []
        for ingredient in self.recipeingredients_set.all():
            food_list.append(calculation_based_by_quantity(
                ingredient.ingredient.get_info(), ingredient.quantity, ingredient.unit.gram
            ))
        total = sum_values_from_dictionary(food_list)
        return total

    def get_nutrition_info_with_portions(self, choosen_portions, max_portions):
        food_list = []
        for ingredient in self.recipeingredients_set.all():
            food_list.append(calculation_based_by_portions(
                ingredient.ingredient.get_info(), ingredient.quantity ,ingredient.unit.gram ,choosen_portions, max_portions
            ))
        total = sum_values_from_dictionary(food_list)
        return total

    def get_ingredients(self):
        return self.recipeingredients_set.all()

    class Meta:
        ordering = ('-created', 'title')

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def compressImage(self, uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        if imageTemproary.format != "jpeg" or imageTemproary.format != "jpg":
            return uploadedImage
        else:
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize((1020, 573))
            imageTemproary.save(outputIoStream, format='JPEG', quality=80)
            outputIoStream.seek(0)
            uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[
                0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
            return uploadedImage

class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(
        Food, on_delete=models.CASCADE, related_name='recipeingredients', db_index=True, verbose_name="Składnik")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, db_index=True)
    unit = models.ForeignKey(
        FoodWeight, on_delete=models.CASCADE, related_name='unit', verbose_name="Rodzaj")
    quantity = models.IntegerField(default=100, db_index=True, verbose_name="Ilość")

    def __str__(self):
        return f"{self.ingredient}--{self.quantity}{self.unit}"


    def get_nutrition_info_based_by_portions(self, meal_portions, choosen_portions):
        return {
            'ingredient': self.ingredient.name,
            'quantity': round((self.quantity / meal_portions * choosen_portions), 2),
            'unit': self.unit.measure_description,
            'gram': round((self.quantity / meal_portions * choosen_portions * self.unit.gram), 2),
        }


class RecipeEvent(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipes")
    portions = models.PositiveIntegerField(default=1, db_index=True)
    description = models.CharField(
        max_length=15, default='Posiłek', db_index=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    date = models.DateField()
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.recipe} consumed by {self.user} on {self.date}"

    class Meta:
        ordering = ['time']
