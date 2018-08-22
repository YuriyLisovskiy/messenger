from django.conf.urls import include, url

appName = 'api'

urlpatterns = [
	url(r'^users/', include('users.urls')),
	url(r'^dialogs/', include('chat.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^auth/', include('authentication.urls'))
]
