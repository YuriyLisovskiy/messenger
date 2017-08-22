from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    user_logo = models.ImageField()
    user_background_photo = models.ImageField()
    user_gender = models.CharField(default="", max_length=6)
    user_birthday_day = models.IntegerField(default=0)
    user_birthday_month = models.CharField(default="", max_length=30)
    user_birthday_year = models.IntegerField(default=0)
    user_country = models.CharField(default="", max_length=30)
    user_city = models.CharField(default="", max_length=50)
    user_mobile_number = models.CharField(default="", max_length=10)
    user_about_me = models.CharField(default="", max_length=999999)
    user_education = models.CharField(default="", max_length=100)

class ChatRoom(models.Model):
    user_author_id = models.CharField(default="", max_length=100)
    user_friend_id = models.CharField(default="", max_length=100)
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

class PhotoLogo(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    photo = models.ImageField()
    upload_time = models.CharField(default="", max_length=100)

class PhotoBackground(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    photo = models.ImageField()
    upload_time = models.CharField(default="", max_length=100)