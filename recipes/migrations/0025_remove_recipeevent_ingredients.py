# Generated by Django 3.1.4 on 2021-02-16 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0024_recipeevent_ingredients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeevent',
            name='ingredients',
        ),
    ]
