from django.conf.urls import url
from . import views


appName = 'account'

urlpatterns = [
	url(r'^edit/id=(?P<profile_id>[0-9]+)/?$', views.EditUserProfile.as_view(), name='edit_profile'),
	url(r'^user/id=(?P<profile_id>[0-9]+)/?$', views.Profile.as_view(), name='profile'),
]
