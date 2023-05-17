from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Recipe

@receiver(m2m_changed, sender=Recipe.liked.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.liked.count()
    instance.save()