from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # 기본 제공되는 필드(예: username, password 등)는 AbstractUser에서 상속받음
    nickname = models.CharField(max_length=30, unique=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    liked_songs = models.ManyToManyField('musics.Song', related_name='liked_by', blank=True)  # 좋아한 노래
    saved_songs = models.ManyToManyField('musics.Song', related_name='saved_by', blank=True)  # 저장한 노래
    shared_songs = models.ManyToManyField('musics.Song', related_name='shared_by', blank=True)  # 공유한 노래
    friends = models.ManyToManyField('self', through='UserRelation', symmetrical=True, related_name='friends_with', blank=True)  # 친구 목록

    class Meta:
        db_table = "users_user"
        ordering = ["nickname"]
    
    def add_friend(self, friend):
        self.friends.add(friend)

    def remove_friend(self, friend):
        self.friends.remove(friend)

    def like_song(self, song):
        if song not in self.liked_songs.all():
            self.liked_songs.add(song)
        else: 
            raise ValidationError("이미 좋아한 노래입니다.")

    def save_song(self, song):
        if song not in self.saved_songs.all():
            self.saved_songs.add(song)
        else:
            raise ValidationError("이미 저장한 노래입니다.")


class UserRelation(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users_user_relation"
        unique_together = (('user1', 'user2'))


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('accepted', '수락됨'),
        ('rejected', '거절됨')
    ]
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = "users_friend_request"
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"

# class UserMessage(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_messages')
#     song = models.ForeignKey("musics.Song", on_delete=models.SET_NULL, null=True)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('like', 'Like'),
        ('save', 'Save'),
        ('comment', 'Comment'),
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
        db_table = "users_user_activity"
        ordering = ['-created_at']  # 최신 활동이 위로 오도록 정렬

    def __str__(self):
        return f'{self.user.username} - {self.activity_type} - {self.created_at}'