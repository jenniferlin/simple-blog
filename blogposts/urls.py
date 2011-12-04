from django.conf.urls.defaults import *
# from blogposts.forms import BlogpostForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('blogposts.views',
    # Examples:
    url(r'^$', 'index'),
    url(r'^create/$', 'create_or_edit'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'create_or_edit'),
    
    # url(r'^comment/$', 'comment'),
    # url(r'^(?P<blog_id>\d+)/comment/$', 'comment'),
    # url(r'^(?P<blog_id>\d+)/vote/$', 'vote'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)