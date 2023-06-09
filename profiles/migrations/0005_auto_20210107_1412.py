# Generated by Django 3.1.4 on 2021-01-07 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_delete_profiledailymeal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollows',
            name='following_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='profiles.profile'),
        ),
        migrations.AlterField(
            model_name='userfollows',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='profiles.profile'),
        ),
    ]
