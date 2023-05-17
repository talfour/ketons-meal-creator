from django.db.models.signals import post_save
from django.dispatch import receiver

from food.models import Food, FoodWeight

@receiver(post_save, sender=Food)
def add_another_object(sender, instance, created, **kwargs):
    if created:
        FoodWeight.objects.create(food_id=instance, measure_description='gram', gram=1.0)
        # Food_Weight.objects.create()