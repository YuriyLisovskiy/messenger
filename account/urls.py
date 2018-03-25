from django.conf.urls import url
from . import views as account_views

appName = 'account'

urlpatterns = [
	url(r'^getProfile/?$', account_views.GetProfile.as_view(), name='get_profile'),
	url(r'^updateProfile/?$', account_views.UpdateProfile.as_view(), name='update_profile'),
]
