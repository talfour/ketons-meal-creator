# Generated by Django 3.1.2 on 2020-12-25 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20201222_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='total_likes',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
