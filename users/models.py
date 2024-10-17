from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    liked_songs = models.ManyToManyField('musics.Song', related_name='liked_by_user', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default="profile_pics/이력서_사진.jpg", blank=True)

    def __str__(self):
        return self.nickname