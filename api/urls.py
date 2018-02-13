from django.conf.urls import include, url

from . import views as api_views
from account import views as account_views

appName = 'api'

urlpatterns = [
	url(r'^chat/', include('chat.urls')),
	url(r'^search/', include('search.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^send/email/?$', api_views.send_email),
	url(r'^login/?$', account_views.LoginView.as_view(), name='login'),
	url(r'^logout/?$', account_views.logout_user, name='logout'),
	url(r'^register/?$', account_views.RegistrationView.as_view(), name='register')
]
