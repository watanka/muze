# Generated by Django 5.1.1 on 2024-10-14 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("musics", "0002_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="song",
            name="album_cover",
            field=models.ImageField(
                default="default_albumcover.png", max_length=200, upload_to=""
            ),
        ),
    ]
