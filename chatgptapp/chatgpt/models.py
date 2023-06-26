from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    context = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user.username}'s Chat"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_question = models.BooleanField(null=False)
    processed = models.BooleanField(null=False)
    deleted = models.BooleanField(null=False)
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat}"


class Answer(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.message}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    vote = models.BooleanField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote from {self.user.username} in {self.message}"