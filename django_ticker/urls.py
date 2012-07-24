from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_ticker.views.home', name='home'),
    # url(r'^django_ticker/', include('django_ticker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^view/(?P<node_id>\d+)$', 'ticker.views.view'),
    url(r'^view/(?P<node_id>\d+).json$', 'ticker.views.graph'),
    url(r'^node/(?P<node_id>\d+)/edit(?:/focus/(?P<focus>\d+))?$', 'ticker.views.nodeedit'),
    url(r'^node/(?P<node_id>\d+)/run$', 'ticker.views.noderun'),
    url(r'^dump/(?P<dump_id>\d+)$', 'ticker.views.dump_view'),
    url(r'^dump/(?P<dump_id>\d+)/run$', 'ticker.views.dump_run'),
    url(r'^dump/(?P<dump_id>\d+)/status$', 'ticker.views.dump_status'),
    url(r'^dump/(?P<dump_id>\d+)/status$', 'ticker.views.dump_status'),
    url(r'^dump/(?P<dump_id>\d+)/focus$', 'ticker.views.dump_focus'),
)
