from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^a/user/new/?$', 'apps.network.views.NewUserJson'),
)
