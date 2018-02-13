from django.conf.urls import url

from chat import views as chat_views

appName = "chat"

urlpatterns = [
    url(r'^manager/?$', chat_views.ChatRoomView.as_view()),
    url(r'^messages/?$', chat_views.ChatListView.as_view(), name='chat'),
]
