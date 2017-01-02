from django.conf.urls.defaults import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ksodjango.views.home', name='home'),
    # url(r'^ksodjango/', include('ksodjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'', include('kso.urls')),
)
