# Generated by Django 3.1.7 on 2021-05-06 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20210413_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.CharField(db_index=True, max_length=150, verbose_name='Nazwa'),
        ),
    ]
