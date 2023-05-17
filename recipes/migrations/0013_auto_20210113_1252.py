# Generated by Django 3.1.4 on 2021-01-13 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210107_1412'),
        ('recipes', '0012_auto_20210106_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='liked',
        ),

        migrations.AddField(
            model_name='recipe',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='likes', through='recipes.Like', to='profiles.Profile'),
        ),
    ]