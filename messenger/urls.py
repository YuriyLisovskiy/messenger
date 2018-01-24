from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from chat import views as chat_views
from account import views as account_views


admin.autodiscover()

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^chat/', include('chat.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^$', chat_views.index, name='index'),
	url(r'^chat_manager/?$', chat_views.ChatManager.as_view()),
	url(r'^send_email/?$', chat_views.send_email),
	url(r'^register/?$', account_views.UserFormView.as_view(), name='register'),
	url(r'^login/?$', account_views.login_user, name='login'),
	url(r'^logout/?$', account_views.logout_user, name='logout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
