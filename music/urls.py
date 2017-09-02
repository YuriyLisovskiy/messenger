from django.conf.urls import url
from . import views


appName = "music"

urlpatterns = [
    url(r'^music/$', views.Music.as_view(), name='music'),
    url(r'^music_manager/$', views.MusicManager.as_view()),
]
