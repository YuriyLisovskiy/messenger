from django.conf.urls import include, url

appName = 'api'

urlpatterns = [
	url(r'^chats/', include('chat.urls')),
	url(r'^users/', include('users.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^auth/', include('authentication.urls'))
]
