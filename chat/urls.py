from django.conf.urls import url
from . import views

appName = "chat"

urlpatterns = [
    url(r'^about/?$', views.index, name='index'),
    url(r'^messages/?$', views.chat, name='chat'),
    url(r'^search/?$', views.SearchPeople.as_view(), name='people'),
]