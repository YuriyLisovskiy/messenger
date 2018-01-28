from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns

from chat import views as chat_views


admin.autodiscover()

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^chat/', include('chat.urls')),
	url(r'^account/', include('account.urls')),
	url(r'^$', chat_views.index, name='index'),
	url(r'^search/', include('search.urls')),
	url(r'^api/', include('api.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
