from django.conf.urls import url

from . import views

appName = 'users'

urlpatterns = [
    url(r'^getUsers/?$', views.GetUsers.as_view(), name='get_users')
]
