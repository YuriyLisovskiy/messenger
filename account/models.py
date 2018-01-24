from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    user_logo = models.ImageField(default='logo_none.jpg')
    user_gender = models.CharField(max_length=6, blank=True)
    user_birthday_day = models.CharField(max_length=2, blank=True)
    user_birthday_month = models.CharField(max_length=2, blank=True)
    user_birthday_year = models.CharField(max_length=4, blank=True)
    user_country = models.CharField(max_length=100, blank=True)
    user_city = models.CharField(max_length=50, blank=True)
    user_mobile_number = models.CharField(max_length=10, blank=True)
    user_about_me = models.CharField(max_length=999999, blank=True)
    user_education = models.CharField(max_length=100, blank=True)
    

class PhotoLogo(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    photo = models.ImageField()
    upload_time = models.CharField(default="", max_length=100)
