from django.conf.urls import url

from . import views

appName = "chat"

urlpatterns = [
    url(r'^about/?$', views.IndexView.as_view(), name='index'),
    url(r'^messages/?$', views.ChatView.as_view(), name='chat'),
]
