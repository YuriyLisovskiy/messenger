from django.conf.urls import url
from . import views as account_views


appName = 'account'

urlpatterns = [
	url(r'^edit/id=(?P<profile_id>[0-9]+)/?$', account_views.EditUserProfile.as_view(), name='edit_profile'),
	url(r'^user/id=(?P<profile_id>[0-9]+)/?$', account_views.Profile.as_view(), name='profile'),
	url(r'^register/?$', account_views.RegistrationView.as_view(), name='register'),
	url(r'^login/?$', account_views.login_user, name='login'),
	url(r'^logout/?$', account_views.logout_user, name='logout'),
]
