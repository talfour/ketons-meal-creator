# Generated by Django 3.1.4 on 2021-02-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_recipe_portions'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeevent',
            name='portions',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
