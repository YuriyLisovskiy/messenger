from django.db import models


class Album(models.Model):
    pass


class Song(models.Model):
    title = models.CharField(default="", max_length=100)
    artist = models.CharField(default="", max_length=100)
    duration = models.FloatField(default=0)
    source = models.FileField(default=1)

