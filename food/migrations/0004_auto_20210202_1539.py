# Generated by Django 3.1.4 on 2021-02-02 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_ingredient_measurementquantity_measurementunits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='unit',
        ),
    ]