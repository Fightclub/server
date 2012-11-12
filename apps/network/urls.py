from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^a/gift/new?$', 'apps.network.views.NewGiftJson'),
    url(r'^a/gift/redeem?$', 'apps.network.views.RedeemGiftJson'),
    url(r'^a/user/new/?$', 'apps.network.views.NewUserJson'),
    url(r'^a/user/login?$', 'apps.network.views.UserLoginJson'),
)
