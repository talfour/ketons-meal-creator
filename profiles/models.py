from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .utils import get_random_code, count_calories, count_micronutrient_keto, count_micronutrient_optimal
from django.template.defaultfilters import slugify
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
# User._meta.get_field('email')._unique = True

class Profile(models.Model):

    """Profile model to add informations about user"""

    ACTIVITY_CHOICES = (
        ('sedentary behaviour', 'Siedzący tryb życia'),
        ('light physical activity', 'Lekka aktywność fizyczna'),
        ('moderate physical activity', 'Średnia aktywność fizyczna'),
        ('vigorous physical activity', 'Intensywna aktywność fizyczna'),
    )
    GENDER_CHOICES = (
        ('female', 'Kobieta'),
        ('male', 'Mężczyzna'),
    )
    DIET_CHOICES = (
        ('keto', 'Keto'),
        ('optimal', 'Optimal'),
    )
    TARGET = (
        ('redukcja', 'Redukcja wagi'),
        ('utrzymanie', 'Utrzymanie wagi'),
        ('masa', 'Zwiększenie masy'),
    )

    first_name = models.CharField(max_length=200, blank=True, verbose_name="Imię")
    last_name = models.CharField(max_length=200, blank=True, verbose_name="Nazwisko")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="brak bio...", max_length=300, verbose_name="Coś o sobie")
    avatar = models.ImageField(default="avatar.png", upload_to="avatars/")
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="Płeć")
    weight = models.IntegerField(default=0, verbose_name="Waga")
    height = models.IntegerField(default=0, verbose_name="Wzrost")
    age = models.IntegerField(default=0, verbose_name="Wiek")
    activity = models.CharField(
        max_length=27, choices=ACTIVITY_CHOICES, default='sedentary behaviour', verbose_name="Aktywność fizyczna")
    want_to_type_nutritiens = models.BooleanField(default=False, verbose_name="Chce sam ustawić kalorie")
    total_kcal = models.IntegerField(blank=True, null=True, verbose_name="Łączna ilość kcal")
    diet_type = models.CharField(
        max_length=7, choices=DIET_CHOICES, default="keto", verbose_name="Typ diety")
    is_on_adaptation = models.BooleanField(default=True)
    proteins = models.IntegerField(blank=True, null=True, verbose_name="Białko")
    carbs = models.IntegerField(blank=True, null=True, verbose_name="Węglowodany")
    fats = models.IntegerField(blank=True, null=True, verbose_name="Tłuszcze")
    target = models.CharField(max_length=10, choices=TARGET, default='utrzymanie', verbose_name="Cel")
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse("profiles:profile-details", kwargs={'slug': self.slug})

    def get_total_profile_nutritiens(self):
        nutritiens = {'total_calories': self.total_kcal, 'proteins': self.proteins,
                      'carbohydrates': self.carbs, 'fats': self.fats}
        return nutritiens

    def get_posts_no(self):
        return self.recipes.all().count()

    def get_all_authors_recipes(self):
        return self.recipes.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_likes = 0
        for like in likes:
            if like.value == 'Like':
                total_likes += 1
        return total_likes

    def get_likes_received(self):
        recipes = self.recipes.all()
        total_likes = 0
        for like in recipes:
            total_likes += like.liked.all().count()
        return total_likes
        
    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                if to_slug == "":
                    to_slug = str(self.user.username)
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user.username)
        self.slug = to_slug

        if self.weight and self.height and self.age and self.gender and self.activity and self.want_to_type_nutritiens is False:
            total_kcal = count_calories(
                self.weight, self.height, self.age, self.gender, self.activity, self.target)
        else:
            total_kcal = 0
        self.total_kcal = total_kcal

        if self.total_kcal and self.diet_type == "keto" and self.want_to_type_nutritiens is False:
            carbs = count_micronutrient_keto(
                self.total_kcal, self.diet_type, self.is_on_adaptation)[0]
            proteins = count_micronutrient_keto(
                self.total_kcal, self.diet_type, self.is_on_adaptation)[1]
            fats = count_micronutrient_keto(
                self.total_kcal, self.diet_type, self.is_on_adaptation)[2]
            self.carbs = carbs
            self.proteins = proteins
            self.fats = fats
        elif self.diet_type == "optimal" and self.want_to_type_nutritiens is False:
            carbs = count_micronutrient_optimal(self.weight)[0]
            proteins = count_micronutrient_optimal(self.weight)[1]
            fats = count_micronutrient_optimal(self.weight)[2]
            self.total_kcal = carbs*4 + proteins*4 + fats*9
            self.carbs = carbs
            self.proteins = proteins
            self.fats = fats
            
        super(Profile, self).save(*args, **kwargs)

    
class UserFollows(models.Model):

    """Following system like in instagram."""

    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='following')
    following_user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def get_following_users(self):
        return self.user_id.all()

    def get_following_users_no(self):
        return self.user_id.all().count()

    def __str__(self):
        return f"{self.following_user_id} is following {self.user_id}"


class Weight(models.Model):
    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="user_weight")
    weight = models.FloatField()
    date = models.DateField(auto_now_add=True)
