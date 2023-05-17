# Generated by Django 3.1.4 on 2021-01-01 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_favouritemeal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favouritemeal',
            name='meal',
        ),
        migrations.AddField(
            model_name='favouritemeal',
            name='meal',
            field=models.ManyToManyField(to='recipes.Recipe'),
        ),
    ]
