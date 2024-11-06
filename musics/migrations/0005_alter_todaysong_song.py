# Generated by Django 5.1.2 on 2024-11-06 00:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0004_todaysong'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todaysong',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='today_song_set', to='musics.song'),
        ),
    ]
