# Generated by Django 3.1.4 on 2021-02-02 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20210113_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ManyToManyField(to='questions.Category'),
        ),
    ]
