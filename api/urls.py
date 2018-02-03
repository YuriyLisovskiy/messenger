from django.conf.urls import url

from . import views as api_views

appName = 'api'

urlpatterns = [
	url(r'^send/email/?$', api_views.send_email),
	url(r'^chat/manager/?$', api_views.Chat.as_view())
]
