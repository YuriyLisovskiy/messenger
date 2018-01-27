from django.conf.urls import url

from . import views as api_views

appName = 'api'

urlpatterns = [
	url(r'^chat/manager/?$', api_views.ChatManager.as_view()),
	url(r'^send/email/?$', api_views.send_email),
]
