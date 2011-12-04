from django.conf.urls.defaults import *


urlpatterns = patterns('profiles.views',
    url(r'^edit/$', 'profile_edit', name='profile_edit'),
    url(r'^(?P<username>[-\w]+)/$','profile_detail', name='profile_detail' ),
)