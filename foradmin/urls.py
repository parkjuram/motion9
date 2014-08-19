from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^manage/shipping/$', 'foradmin.views.manage_shipping_view', name='manage_shipping'),
)