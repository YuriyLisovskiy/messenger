from django.conf.urls import url
from . import views

appName = "chat"

urlpatterns = [
    url(r'^about/$', views.index, name='index'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^profile/edit/$', views.EditUserProfile.as_view(), name='edit_profile'),
    url(r'^user/(?P<profile_id>[0-9]+)/$', views.Profile.as_view(), name='profile'),
    url(r'^search/$', views.SearchPeople.as_view(), name='people'),
]