# Generated by Django 3.1.7 on 2021-04-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_delete_gki'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activity',
            field=models.CharField(choices=[('sedentary behaviour', 'Siedzący tryb życia'), ('light physical activity', 'Lekka aktywność fizyczna'), ('moderate physical activity', 'Średnia aktywność\xa0fizyczna'), ('vigorous physical activity', 'Intensywna aktywność\xa0fizyczna')], default='sedentary behaviour', max_length=27, verbose_name='Aktywność fizyczna'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=0, verbose_name='Wiek'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='brak bio...', max_length=300, verbose_name='Coś o sobie'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='carbs',
            field=models.IntegerField(blank=True, null=True, verbose_name='Węglowodany'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='diet_type',
            field=models.CharField(choices=[('keto', 'Keto'), ('optimal', 'Optimal')], default='keto', max_length=7, verbose_name='Typ diety'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fats',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tłuszcze'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, default=' ', max_length=200, verbose_name='Imię'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('female', 'Kobieta'), ('male', 'Mężczyzna')], default='female', max_length=6, verbose_name='Płeć'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.IntegerField(default=0, verbose_name='Wzrost'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, default=' ', max_length=200, verbose_name='Nazwisko'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='proteins',
            field=models.IntegerField(blank=True, null=True, verbose_name='Białko'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='total_kcal',
            field=models.IntegerField(blank=True, null=True, verbose_name='Łączna ilość\xa0kcal'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='want_to_type_nutritiens',
            field=models.BooleanField(default=False, verbose_name='Chce sam ustawić kalorie'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Waga'),
        ),
    ]