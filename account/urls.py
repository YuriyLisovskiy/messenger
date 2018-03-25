from django.conf.urls import url
from . import views as account_views
from authentication import views as auth_views


appName = 'account'

urlpatterns = [
	url(r'^getUser/?$', account_views.Profile.as_view(), name='get_user'),
	url(r'^checkEmail/?$', auth_views.CheckEmail.as_view(), name='check_email'),
	url(r'^editProfile/?$', account_views.EditProfile.as_view(), name='edit_profile')
]
