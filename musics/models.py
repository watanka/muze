from django.db import models
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
    # album_cover =  models.ImageField(upload_to='album_cover/', max_length=200, default='default_albumcover.png')
    album_cover = models.URLField()
    artist = models.CharField(max_length = 100)
    genre = models.CharField(max_length=20, choices = GENRE_CHOICES, blank=True)
    release_date = models.DateField()
    num_mention = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.album_cover.startswith('http'):
            self.album_cover = unquote(self.album_cover)
        super(Song, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.artist}"
    
class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("users.User", on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.song.title} - {self.created_at}'