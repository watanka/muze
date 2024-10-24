# Generated by Django 5.1.1 on 2024-10-15 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("musics", "0004_alter_song_album_cover_alter_song_genre"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="liked_songs",
            field=models.ManyToManyField(
                blank=True, related_name="liked_by_user", to="musics.song"
            ),
        ),
    ]
