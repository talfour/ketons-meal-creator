# Generated by Django 3.1.2 on 2020-11-11 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        ('profiles', '0001_initial'),
        ('food', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledailymeal',
            name='food',
            field=models.ManyToManyField(blank=True, null=True, related_name='recipe_day', to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='profiledailymeal',
            name='ingredients',
            field=models.ManyToManyField(blank=True, null=True, related_name='food_day', to='food.Food'),
        ),
        migrations.AddField(
            model_name='profiledailymeal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
