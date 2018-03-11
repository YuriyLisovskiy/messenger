from django.conf.urls import url

from chat import views as chat_views

appName = 'chat'

urlpatterns = [
    url(r'^messages/?$', chat_views.ChatRoomView.as_view(), name='messages'),
    url(r'^chats/?$', chat_views.ChatListView.as_view(), name='chats'),
]
