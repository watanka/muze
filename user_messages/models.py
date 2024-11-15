from django.db import models

class MessageManager(models.Manager):

    def save_message(self, sender, receiver, song, content):
        message = self.create(sender=sender, receiver=receiver, song=song, content=content)
        return message

    def get_unread_messages(self, user):
        return self.filter(receiver=user, is_read=False)

    def list_inbox(self, user):
        return self.filter(receiver=user).order_by('is_read', '-timestamp')

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
    
    class Meta:
        db_table = "user_messages_message"
        get_latest_by = ("timestamp", )
        ordering = ["-timestamp"]

    objects = MessageManager()

    def read_message(self):
        self.is_read = True
        self.save(update_fields=['is_read'])

