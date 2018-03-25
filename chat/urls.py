from django.conf.urls import url

from chat import views as chat_views

appName = 'chat'

urlpatterns = [
    url(r'^getChats/?$', chat_views.ChatListView.as_view(), name='get_chats'),
    url(r'^getMessages/?$', chat_views.ChatRoomView.as_view(), name='get_messages'),
    url(r'^sendMessage/?$', chat_views.ChatRoomView.as_view(), name='send_message')
]
