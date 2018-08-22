from django.conf.urls import url

from chat import views as chat_views

appName = 'chat'

urlpatterns = [
    url(r'^getChats/?$', chat_views.GetChats.as_view(), name='get_chats'),
    url(r'^deleteChat/?$', chat_views.DeleteChat.as_view(), name='delete_chat'),
    url(r'^getMessages/?$', chat_views.GetMessages.as_view(), name='get_messages'),
    url(r'^sendMessage/?$', chat_views.SendMessage.as_view(), name='send_message')
]
