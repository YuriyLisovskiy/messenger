from django.db import models
from chat.models import UserProfile


class Album(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    title = models.CharField(default="", max_length=100)
    artist = models.CharField(default="", max_length=100)
    logo = models.ImageField(default=1)
    description = models.CharField(default="", max_length=500, blank=True)


class Song(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=1)
    title = models.CharField(default="", max_length=100)
    artist = models.CharField(default="", max_length=100)
    source = models.FileField(default=1)

