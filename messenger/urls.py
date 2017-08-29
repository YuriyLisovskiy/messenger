from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from chat import views


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('chat.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^', include('music.urls')),
    url(r'^chat_manager/$', views.ChatManager.as_view()),
    url(r'^send_email/$', views.send_email),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.login_user, name='login')
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
