from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

from api import views as api_views


admin.autodiscover()

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^api/v1/', include('api.urls')),
	url(r'^$', api_views.IndexView.as_view(), name='index'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
