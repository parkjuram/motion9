from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^registration$', 'users.views.registration_view', name='registration'),
    # url(r'^login$', 'users.views.login_view', name='login'),
    # url(r'^logout$', 'users.views.logout_view', name='logout'),
    # url(r'^update$', 'users.views.update_view', name='update'),
)