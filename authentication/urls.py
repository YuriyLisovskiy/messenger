from django.conf.urls import url

from . import views as auth_views

appName = 'authentication'

urlpatterns = [
	url(r'^signIn/?$', auth_views.SignIn.as_view(), name='sign_in'),
	url(r'^singUp/?$', auth_views.SignUp.as_view(), name='sign_up'),
	url(r'^signOut/?$', auth_views.SignOut.as_view(), name='sign_out'),
	url(r'^sendEmail/?$', auth_views.SendEmail.as_view(), name='send_email'),
	url(r'^checkEmail/?$', auth_views.CheckEmail.as_view(), name='check_email')
]