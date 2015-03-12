from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'motion9.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('users.urls')),
    url(r'', include('web.urls')),
    url(r'mobile/', include('mobile.urls', namespace='mobile')),
    url(r'foradmin/', include('foradmin.urls', namespace='foradmin')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^supervisor/', include('supervisor.urls', namespace='supervisor')),
    url(r'^common/', include('common.urls', namespace='common')),
    url(r'^accounts/', include('allauth.urls')),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)