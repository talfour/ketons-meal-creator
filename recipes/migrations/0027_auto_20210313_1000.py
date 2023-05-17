# Generated by Django 3.1.4 on 2021-03-13 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_gki'),
        ('recipes', '0026_auto_20210223_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='liked',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='likes', through='recipes.Like', to='profiles.Profile'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='saved',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='saves', to='profiles.Profile'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='recipeevent',
            name='description',
            field=models.CharField(db_index=True, default='Meal', max_length=15),
        ),
        migrations.AlterField(
            model_name='recipeevent',
            name='portions',
            field=models.PositiveIntegerField(db_index=True, default=1),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='quantity',
            field=models.IntegerField(db_index=True, default=100),
        ),
    ]
