from django.conf.urls import url

from chat import views as chat_views

appName = "chat"

urlpatterns = [
    url(r'^manager/?$', chat_views.Chat.as_view()),
    url(r'^messages/?$', chat_views.ChatView.as_view(), name='chat'),
]
