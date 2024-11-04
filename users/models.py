from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # 기본 제공되는 필드(예: username, password 등)는 AbstractUser에서 상속받음
    nickname = models.CharField(max_length=30, unique=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    today_song = models.ForeignKey('musics.Song', on_delete=models.SET_NULL, null=True, blank=True)  # 오늘의 노래
    liked_songs = models.ManyToManyField('musics.Song', related_name='liked_by', blank=True)  # 좋아한 노래
    saved_songs = models.ManyToManyField('musics.Song', related_name='saved_by', blank=True)  # 저장한 노래
    shared_songs = models.ManyToManyField('musics.Song', related_name='shared_by', blank=True)  # 공유한 노래
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends_with', blank=True)  # 친구 목록

    def add_friend(self, friend):
        self.friends.add(friend)
    
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('like', 'Like'),
        ('save', 'Save'),
        ('share', 'Share'),
        ('set_today_song', 'Set Today Song'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    song = models.ForeignKey('musics.Song', null=True, blank=True, on_delete=models.SET_NULL, related_name='user_activities')
    friend_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='friend_activities')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # 최신 활동이 위로 오도록 정렬

    def __str__(self):
        return f'{self.user.username} - {self.activity_type} - {self.created_at}'