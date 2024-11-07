from django.db import models
from datetime import timedelta, datetime
from urllib.parse import unquote

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
    track_popularity = models.IntegerField(default=0)
    album_cover = models.URLField()
    album_name = models.CharField(max_length = 200)
    artists = models.CharField(max_length = 100)
    genre = models.CharField(max_length=20, choices = GENRE_CHOICES, blank=True)
    release_date = models.DateField()
    num_mention = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)
    spotify_url = models.URLField()

    def __str__(self):
        return f"{self.title} by {self.artist}"
    
class TodaySong(models.Model):
    user = models.ForeignKey("users.User", on_delete = models.CASCADE, related_name="today_song_set")
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()  # 현재 시간 설정
        if not self.expired_at:
            self.expired_at = self.created_at + timedelta(hours=24)
        super().save(*args, **kwargs)


class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("users.User", on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.song.title} - {self.created_at}'