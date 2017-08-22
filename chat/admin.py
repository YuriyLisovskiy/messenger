from django.contrib import admin
from .models import UserProfile, Message, ChatRoom, PhotoLogo, PhotoBackground

admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(ChatRoom)
admin.site.register(PhotoLogo)
admin.site.register(PhotoBackground)
