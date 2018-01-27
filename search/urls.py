from django.conf.urls import url

from . import views

appName = 'search'

urlpatterns = [
    url(r'^people/?$', views.SearchPeople.as_view(), name='people')
]
