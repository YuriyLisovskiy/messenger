from django.db import models
from account.models import UserProfile


class ChatRoom(models.Model):
    user_author_id = models.CharField(default="", max_length=255)
    user_friend_id = models.CharField(default="", max_length=255)
    author = models.ForeignKey(UserProfile, null=True, related_name='author')
    friend = models.ForeignKey(UserProfile, null=True, related_name='friend')
    logo = models.ImageField(default=1)


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, default=1)
    msg = models.CharField(default="", max_length=99999)
    author = models.CharField(default="", max_length=100)
    time = models.CharField(default="", max_length=100)
    author_fn_ln = models.CharField(default="", max_length=100)
    author_logo = models.FileField(default=1)
    author_id = models.CharField(default="", max_length=100)
