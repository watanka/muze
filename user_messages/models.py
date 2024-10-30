from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    receiver = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name='received_messages')
    song = models.ForeignKey("musics.Song", on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"