from django.db import models
from datetime import timedelta, datetime
from urllib.parse import unquote
from django.db.models import Count

class SongManager(models.Manager):
    def list_by(self, order_type):
        if order_type == 'release_date':
            method = '-release_date'
            self.get_queryset().order_by(method)
        elif order_type == 'num_likes':
            method = '-num_likes'
            self.get_queryset().order_by(method)
        elif order_type == 'num_mentions':
            method = '-num_mention'
            self.get_queryset().order_by(method)
        elif order_type == 'num_comments':
            method = '-num_comments'
            self.get_queryset().annotate(num_comments=Count('comments')).order_by(method)
        else:
            raise ValueError(f"Invalid order type: {order_type}")
        
        return self.get_queryset().order_by(method)

    def search(self, keyword, category):
        return self.filter(**{f'{category}__icontains': keyword})
    

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
    title = models.CharField(max_length = 200, help_text="음악 제목")
    track_popularity = models.IntegerField(default=0, help_text="음악 인기도")
    album_cover = models.URLField(help_text="앨범 커버 이미지 URL") # TODO: 이미지 저장 수정
    album_name = models.CharField(max_length = 200, help_text="앨범 이름")
    artists = models.CharField(max_length = 100, help_text="아티스트")
    genre = models.CharField(max_length=20, choices = GENRE_CHOICES, blank=True, help_text="장르")
    release_date = models.DateField(help_text="발매일")
    num_mention = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)
    spotify_url = models.URLField()

    objects = SongManager()

    def __str__(self):
        return f"{self.title} by {self.artists}"
    
    class Meta:
        abstract = False
        managed = True
        proxy = False

        db_table = "musics_song"
        get_latest_by = "release_date"
        ordering = ["-release_date", "title"]

        # TODO: Index 추가
    
    def add_num_likes(self):
        self.num_likes += 1
        self.save(update_fields=['num_likes'])

    def add_num_mention(self):
        self.num_mention += 1
        self.save(update_fields=['num_mention'])

    
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

    class Meta:
        db_table = "musics_today_song"
    
    def is_active(self) -> bool:
        return self.expired_at > datetime.now()

class CommentManager(models.Manager):
    def save_comment(self, song, user, content):
        comment = self.create(song=song, user=user, content=content)
        return comment

class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("users.User", on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return f'{self.user} - {self.song.title} - {self.created_at}'
    
    class Meta:
        db_table = "musics_comment"
        get_latest_by = "created_at"
        ordering = ["-created_at"]

    

