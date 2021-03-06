from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fightclub.views.home', name='home'),
    # url(r'^fightclub/', include('fightclub.foo.urls')),
    url(r'^catalog/', include('apps.catalog.urls')),
    url(r'^network/', include('apps.network.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/django_rq/', include('django_rq.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
