from django.conf.urls import url

from . import views

appName = 'users'

urlpatterns = [
    url(r'^getUsers/?$', views.SearchPeople.as_view(), name='people')
]
