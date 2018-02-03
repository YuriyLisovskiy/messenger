from django.conf.urls import url
from . import views as account_views


appName = 'account'

urlpatterns = [
	url(r'^user/id=(?P<profile_id>[0-9]+)/edit/?$', account_views.EditUserProfile.as_view(), name='edit_profile'),
	url(r'^user/id=(?P<profile_id>[0-9]+)/?$', account_views.Profile.as_view(), name='profile')
]
