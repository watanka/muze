# Generated by Django 5.1.1 on 2024-10-08 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("album_cover", models.ImageField(max_length=200, upload_to="")),
                ("artist", models.CharField(max_length=100)),
                (
                    "genre",
                    models.CharField(
                        choices=[
                            ("POP", "Pop"),
                            ("ROCK", "Rock"),
                            ("HIPHOP", "Hip Hop"),
                            ("R&B", "R&B"),
                            ("JAZZ", "Jazz"),
                            ("CLASSICAL", "Classical"),
                            ("COUNTRY", "Country"),
                            ("REGGAE", "Reggae"),
                            ("ELECTRONIC", "Electronic"),
                            ("METAL", "Metal"),
                        ],
                        max_length=20,
                    ),
                ),
                ("release_date", models.DateField()),
            ],
        ),
    ]
