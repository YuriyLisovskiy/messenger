from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

from chat import views as chat_views
from account import views as account_views


admin.autodiscover()

urlpatterns = [
	url(r'^$', chat_views.index, name='index'),
	url(r'^api/', include('api.urls')),
	url(r'^chat/', include('chat.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^search/', include('search.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^login/?$', account_views.login_user, name='login'),
	url(r'^logout/?$', account_views.logout_user, name='logout'),
	url(r'^register/?$', account_views.RegistrationView.as_view(), name='register'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
