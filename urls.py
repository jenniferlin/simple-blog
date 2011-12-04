from django.conf.urls.defaults import *
from settings import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'blogposts.views.index'),
    url(r'^blogposts/', include('blogposts.urls')),
    url(r'^profiles/', include('profiles.urls')),
    
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logged_out.html'}), 
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}), 
    url(r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': '/blogposts/'}), 
    url(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/blogposts/'}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
