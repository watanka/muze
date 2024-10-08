from django.db import models

# Create your models here.
class Song(models.Model):
    GENRE_CHOICES = [
        ('POP', 'Pop'),
        ('ROCK', 'Rock'),
        ('HIPHOP', 'Hip Hop'),
        ('R&B', 'R&B'),
        ('JAZZ', 'Jazz'),
        ('CLASSICAL', 'Classical'),
        ('COUNTRY', 'Country'),
        ('REGGAE', 'Reggae'),
        ('ELECTRONIC', 'Electronic'),
        ('METAL', 'Metal'),
        # 필요에 따라 더 많은 장르 추가
    ]
    title = models.CharField(max_length = 200)
    album_cover =  models.ImageField(max_length=200)
    artist = models.CharField(max_length = 100)
    genre = models.CharField(max_length=20, choices = GENRE_CHOICES)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.title} by {self.artist}"