# Generated by Django 3.1.7 on 2021-04-13 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_auto_20210319_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='folate_dfe',
        ),
        migrations.RemoveField(
            model_name='food',
            name='folic_acid',
        ),
        migrations.RemoveField(
            model_name='food',
            name='food_folate',
        ),
        migrations.RemoveField(
            model_name='food',
            name='vit_a_rae',
        ),
        migrations.AlterField(
            model_name='food',
            name='alpha_carot',
            field=models.FloatField(default=0, verbose_name='Alfa karoten'),
        ),
        migrations.AlterField(
            model_name='food',
            name='ash',
            field=models.FloatField(default=0, verbose_name='Popiół'),
        ),
        migrations.AlterField(
            model_name='food',
            name='beta_carot',
            field=models.FloatField(default=0, verbose_name='Beta karoten'),
        ),
        migrations.AlterField(
            model_name='food',
            name='beta_crypt',
            field=models.FloatField(default=0, verbose_name='Beta-kryptoksantyna'),
        ),
        migrations.AlterField(
            model_name='food',
            name='calcium',
            field=models.FloatField(default=0, verbose_name='Wapń'),
        ),
        migrations.AlterField(
            model_name='food',
            name='carbs',
            field=models.FloatField(default=0, verbose_name='Węglowodany'),
        ),
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.CharField(choices=[('produkty mleczne i jajeczne', 'Produkty mleczne i jajeczne'), ('produkty wolowe', 'Produkty wołowe'), ('ziarna zboz i makaron', 'Ziarna zbóż i makaron'), ('tluszcze i oleje', 'Tłuszcze i oleje'), ('produkty z ryb i skorupiakow', 'Produkty z ryb i skorupiaków'), ('owoce', 'Owoce'), ('produkty z jagnieciny, cieleciny i dziczyzny', 'Produkty z jagnięciny, cielęciny i dziczyzny'), ('rosliny straczkowe i produkty z roslin straczkowych', 'Rośliny strączkowe i produkty z roślin strączkowych'), ('ziarna i orzechy', 'Ziarna i orzechy'), ('produkty wieprzowe', 'Produkty wieprzowe'), ('produkty drobiowe', 'Produkty drobiowe'), ('przyprawy i ziola', 'Przyprawy i zioła'), ('warzywa i produkty warzywne', 'Warzywa i produkty warzywne'), ('wedliny', 'Wędliny'), ('pieczywo', 'Pieczywo'), ('przetwory rybne', 'Przetwory rybne')], max_length=80, verbose_name='Kategoria'),
        ),
        migrations.AlterField(
            model_name='food',
            name='cholesterol',
            field=models.FloatField(default=0, verbose_name='Cholesterol'),
        ),
        migrations.AlterField(
            model_name='food',
            name='choline',
            field=models.FloatField(default=0, verbose_name='Cholina'),
        ),
        migrations.AlterField(
            model_name='food',
            name='copper',
            field=models.FloatField(default=0, verbose_name='Miedź'),
        ),
        migrations.AlterField(
            model_name='food',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Utworzono'),
        ),
        migrations.AlterField(
            model_name='food',
            name='fats',
            field=models.FloatField(default=0, verbose_name='Tłuszcze'),
        ),
        migrations.AlterField(
            model_name='food',
            name='fats_mono',
            field=models.FloatField(default=0, verbose_name='Tłuszcze jednonienasycone'),
        ),
        migrations.AlterField(
            model_name='food',
            name='fats_poly',
            field=models.FloatField(default=0, verbose_name='Tłuszcze nienasycone'),
        ),
        migrations.AlterField(
            model_name='food',
            name='fats_saturated',
            field=models.FloatField(default=0, verbose_name='Tłuszcze nasycone'),
        ),
        migrations.AlterField(
            model_name='food',
            name='fiber',
            field=models.FloatField(default=0, verbose_name='Błonnik'),
        ),
        migrations.AlterField(
            model_name='food',
            name='folate',
            field=models.FloatField(default=0, verbose_name='Kwas foliowy (B9)'),
        ),
        migrations.AlterField(
            model_name='food',
            name='iron',
            field=models.FloatField(default=0, verbose_name='Żelazo'),
        ),
        migrations.AlterField(
            model_name='food',
            name='kcal',
            field=models.FloatField(default=0, verbose_name='Kalorie'),
        ),
        migrations.AlterField(
            model_name='food',
            name='lut_and_zea',
            field=models.FloatField(default=0, verbose_name='Luteina i Zeaksantyna'),
        ),
        migrations.AlterField(
            model_name='food',
            name='lycopene',
            field=models.FloatField(default=0, verbose_name='Likopen'),
        ),
        migrations.AlterField(
            model_name='food',
            name='magnesium',
            field=models.FloatField(default=0, verbose_name='Magnez'),
        ),
        migrations.AlterField(
            model_name='food',
            name='manganese',
            field=models.FloatField(default=0, verbose_name='Mangan'),
        ),
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='food',
            name='net_carbs',
            field=models.FloatField(default=0, verbose_name='Węglowodany netto'),
        ),
        migrations.AlterField(
            model_name='food',
            name='niacin',
            field=models.FloatField(default=0, verbose_name='Niacyna (B3)'),
        ),
        migrations.AlterField(
            model_name='food',
            name='panto_acid',
            field=models.FloatField(default=0, verbose_name='Kwas pantotenowy (B5)'),
        ),
        migrations.AlterField(
            model_name='food',
            name='phosphorus',
            field=models.FloatField(default=0, verbose_name='Fosfor'),
        ),
        migrations.AlterField(
            model_name='food',
            name='potassium',
            field=models.FloatField(default=0, verbose_name='Potas'),
        ),
        migrations.AlterField(
            model_name='food',
            name='proteins',
            field=models.FloatField(default=0, verbose_name='Białko'),
        ),
        migrations.AlterField(
            model_name='food',
            name='retinol',
            field=models.FloatField(default=0, verbose_name='Retinol'),
        ),
        migrations.AlterField(
            model_name='food',
            name='riboflavin',
            field=models.FloatField(default=0, verbose_name='Ryboflawina (B2)'),
        ),
        migrations.AlterField(
            model_name='food',
            name='selenium',
            field=models.FloatField(default=0, verbose_name='Selen'),
        ),
        migrations.AlterField(
            model_name='food',
            name='sodium',
            field=models.FloatField(default=0, verbose_name='Sód'),
        ),
        migrations.AlterField(
            model_name='food',
            name='sugar',
            field=models.FloatField(default=0, verbose_name='Cukier'),
        ),
        migrations.AlterField(
            model_name='food',
            name='thiamin',
            field=models.FloatField(default=0, verbose_name='Tiamina (B1)'),
        ),
        migrations.AlterField(
            model_name='food',
            name='vid_d_iu',
            field=models.FloatField(default=0, verbose_name='Witamina D(iu)'),
        ),
        migrations.AlterField(
            model_name='food',
            name='vit_a',
            field=models.FloatField(default=0, verbose_name='Witamina A'),
        ),
        migrations.AlterField(
            model_name='food',
            name='vit_b12',
            field=models.FloatField(default=0, verbose_name='Witamina B12'),
        ),
        migrations.AlterField(
            model_name='food',
            name='vit_b6',
            field=models.FloatField(default=0, verbose_name='Witamina B6'),
        ),
        migrations.AlterField(
            model_name='food',
            name='vit_c',
            field=models.FloatField(default=0, verbose_name='Witamina C'),
        ),
        migrations.AlterField(
            model_name='food',
            name='vit_d',
            field=models.FloatField(default=0, verbose_name='Witamina D(μg)'),
        ),
        migrations.AlterField(
            model_name='food',
            name='vit_e',
            field=models.FloatField(default=0, verbose_name='Witamina E'),
        ),
        migrations.AlterField(
            model_name='food',
            name='vit_k',
            field=models.FloatField(default=0, verbose_name='Witamina K'),
        ),
        migrations.AlterField(
            model_name='food',
            name='water',
            field=models.FloatField(default=0, verbose_name='Woda'),
        ),
        migrations.AlterField(
            model_name='food',
            name='zinc',
            field=models.FloatField(default=0, verbose_name='Cynk'),
        ),
    ]
