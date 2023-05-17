from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .models import Profile
from .utils import get_random_code

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):

    __initial_first_name = None
    __initial_last_name = None
    if created:
        Profile.objects.create(user=instance)
        # profile = Profile.objects.get(user=instance)

        # ex = False
        # to_slug = profile.user.username
        # to_slug = slugify(to_slug + " " + str(get_random_code()))
        # ex = Profile.objects.filter(slug=to_slug).exists()
        # while ex:
        #     to_slug = slugify(to_slug + " " + str(get_random_code()))
        #     ex = Profile.objects.filter(slug=to_slug).exists()
        # profile.slug = to_slug