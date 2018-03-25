from django.conf.urls import url
from . import views as account_views

appName = 'account'

urlpatterns = [
	url(r'^getUser/?$', account_views.GetUser.as_view(), name='get_user'),
	url(r'^updateProfile/?$', account_views.UpdateProfile.as_view(), name='update_profile'),
]
