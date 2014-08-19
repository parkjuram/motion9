from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'motion9.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('users.urls')),
    url(r'', include('web.urls')),
    url(r'mobile/', include('mobile.urls')),
    url(r'foradmin/', include('foradmin.urls', namespace='foradmin')),
    url(r'^accounts/', include('registration.backends.default.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)