from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gameoflife.views.home', name='home'),
    # url(r'^gameoflife/', include('gameoflife.foo.urls')),

    url(r'^$', 'world.views.index', name='site_index'),
    url(r'^(?P<slug>[-a-z0-9_]+)/$', 'world.views.detail', name='detail'),
    url(r'^(?P<slug>[-a-z0-9_]+)/(?P<lat>\d+)/(?P<long>\d+)/$', 'world.views.detail', name='detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
