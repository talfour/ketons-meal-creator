# Generated by Django 3.1.4 on 2021-01-13 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210107_1412'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='votes1',
        ),
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.ManyToManyField(related_name='votes', through='questions.VoteSystem', to='profiles.Profile'),
        ),
    ]
