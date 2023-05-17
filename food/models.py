from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.shortcuts import reverse
from profiles.models import Profile

# Create your models here.


class Food(models.Model):
    """Food model"""
    FOODCATEGORIES = (
        ('produkty mleczne i jajeczne', 'Produkty mleczne i jajeczne'),
        ('produkty wolowe', 'Produkty wołowe'),
        ('ziarna zboz i makaron', 'Ziarna zbóż i makaron'),
        ('tluszcze i oleje', 'Tłuszcze i oleje'),
        ('produkty z ryb i skorupiakow', 'Produkty z ryb i skorupiaków'),
        ('owoce', 'Owoce'),
        ('produkty z jagnieciny, cieleciny i dziczyzny',
         'Produkty z jagnięciny, cielęciny i dziczyzny'),
        ('rosliny straczkowe i produkty z roslin straczkowych',
         'Rośliny strączkowe i produkty z roślin strączkowych'),
        ('ziarna i orzechy', 'Ziarna i orzechy'),
        ('produkty wieprzowe', 'Produkty wieprzowe'),
        ('produkty drobiowe', 'Produkty drobiowe'),
        ('przyprawy i ziola', 'Przyprawy i zioła'),
        ('warzywa i produkty warzywne', 'Warzywa i produkty warzywne'),
        ('wedliny', 'Wędliny'),
        ('pieczywo', 'Pieczywo'),
        ('przetwory rybne', 'Przetwory rybne'),
        ('slodziki', 'Słodziki'),
        ('inne', 'Inne'),
    )
    name = models.CharField(max_length=150, db_index=True, verbose_name="Nazwa")
    category = models.CharField(choices=FOODCATEGORIES, max_length=80, verbose_name="Kategoria")
    water = models.FloatField(default=0, verbose_name="Woda")
    kcal = models.FloatField(default=0, verbose_name="Kalorie")
    proteins = models.FloatField(default=0, verbose_name="Białko")
    carbs = models.FloatField(default=0, verbose_name="Węglowodany")
    fats = models.FloatField(default=0, verbose_name="Tłuszcze")
    fiber = models.FloatField(default=0, verbose_name="Błonnik")
    sugar = models.FloatField(default=0, verbose_name="Cukier")
    ash = models.FloatField(default=0, verbose_name="Popiół")
    net_carbs = models.FloatField(default=0, verbose_name="Węglowodany netto")
    calcium = models.FloatField(default=0, verbose_name="Wapń")
    iron = models.FloatField(default=0, verbose_name="Żelazo")
    magnesium = models.FloatField(default=0, verbose_name="Magnez")
    phosphorus = models.FloatField(default=0, verbose_name="Fosfor")
    potassium = models.FloatField(default=0, verbose_name="Potas")
    sodium = models.FloatField(default=0, verbose_name="Sód")
    zinc = models.FloatField(default=0, verbose_name="Cynk")
    copper = models.FloatField(default=0, verbose_name="Miedź")
    manganese = models.FloatField(default=0, verbose_name="Mangan")
    selenium = models.FloatField(default=0, verbose_name="Selen")
    vit_c = models.FloatField(default=0, verbose_name="Witamina C")
    thiamin = models.FloatField(default=0, verbose_name="Tiamina (B1)")
    riboflavin = models.FloatField(default=0, verbose_name="Ryboflawina (B2)")
    niacin = models.FloatField(default=0, verbose_name="Niacyna (B3)")
    panto_acid = models.FloatField(default=0, verbose_name="Kwas pantotenowy (B5)")
    vit_b6 = models.FloatField(default=0, verbose_name="Witamina B6")
    folate = models.FloatField(default=0, verbose_name="Kwas foliowy (B9)")
    choline = models.FloatField(default=0, verbose_name="Cholina")
    vit_b12 = models.FloatField(default=0, verbose_name="Witamina B12")
    vit_a = models.FloatField(default=0, verbose_name="Witamina A")
    retinol = models.FloatField(default=0, verbose_name="Retinol")
    alpha_carot = models.FloatField(default=0, verbose_name="Alfa karoten")
    beta_carot = models.FloatField(default=0, verbose_name="Beta karoten")
    beta_crypt = models.FloatField(default=0, verbose_name="Beta-kryptoksantyna")
    lycopene = models.FloatField(default=0, verbose_name="Likopen")
    lut_and_zea = models.FloatField(default=0, verbose_name="Luteina i Zeaksantyna")
    vit_e = models.FloatField(default=0, verbose_name="Witamina E")
    vit_d = models.FloatField(default=0, verbose_name="Witamina D(μg)")
    vid_d_iu = models.FloatField(default=0, verbose_name="Witamina D(iu)")
    vit_k = models.FloatField(default=0, verbose_name="Witamina K")
    fats_saturated = models.FloatField(default=0, verbose_name="Tłuszcze nasycone")
    fats_mono = models.FloatField(default=0, verbose_name="Tłuszcze jednonienasycone")
    fats_poly = models.FloatField(default=0, verbose_name="Tłuszcze nienasycone")
    cholesterol = models.FloatField(default=0, verbose_name="Cholesterol")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Utworzono")
    slug = models.SlugField(max_length=255)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="foods", default=1)

    class Meta():
        ordering = 'name',

    def save(self, *args, **kwargs):
        if not self.slug:
            self.created = timezone.now()
            self.slug = slugify(
                str(self.name + " " + self.created.strftime('%d-%m-%Y')))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('food:food-list')

    def get_info(self):
        values = {
                  'Kalorie': self.kcal,
                  'Białko': self.proteins,
                  'Węglowodany': self.carbs,
                  'Cukier': self.sugar,
                  'Węglowodany netto': self.net_carbs,
                  'Błonnik': self.fiber,
                  'Tłuszcze': self.fats,
                  'Tłuszcze nasycone': self.fats_saturated,
                  'Tłuszcze jednonienasycone': self.fats_mono,
                  'Tłuszcze nienasycone': self.fats_poly,
                  'Cholesterol': self.cholesterol,
                  'Woda': self.water,
                  'Popiuł': self.ash,
                  'Wapń': self.calcium,
                  'Żelazo': self.iron,
                  'Magnez': self.magnesium,
                  'Fosfor': self.phosphorus,
                  'Potas': self.potassium,
                  'Sód': self.sodium,
                  'Cynk': self.zinc,
                  'Miedź': self.copper,
                  'Mangan': self.manganese,
                  'Selen': self.selenium,
                  'Cholina': self.choline,   
                  'Retinol': self.retinol,
                  'Alfa karoten': self.alpha_carot,
                  'Beta karoten': self.beta_carot,
                  'Beta-kryptoksantyna': self.beta_crypt,
                  'Likopen': self.lycopene,
                  'Luteina i Zeaksantyna': self.lut_and_zea,
                  'Witamina A': self.vit_a,
                  'Tiamina (B1)': self.thiamin,
                  'Ryboflawina (B2)': self.riboflavin,
                  'Niacyna (B3)': self.niacin,
                  'Kwas pantotenowy (B5)': self.panto_acid,
                  'Witamina B6': self.vit_b6,
                  'Kwas foliowy (B9)': self.folate,
                  'Witamina B12': self.vit_b12,
                  'Witamina C': self.vit_c,
                  'Witamina D': self.vit_d,
                  'Witamina D iu': self.vid_d_iu,
                  'Witamina E': self.vit_e,
                  'Witamina K': self.vit_k}                
        return values


class FoodWeight(models.Model):
    food_id = models.ForeignKey(
        Food, on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    measure_description = models.CharField(
        max_length=30)
    gram = models.FloatField()

    def __str__(self):
        return f'{self.measure_description}'
