from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('blogposts.views',
    # Examples:
    url(r'^$', 'index'),
    url(r'^create/$', 'create_or_edit'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'create_or_edit'),
    
)