from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    #url(r'^/?$', 'apps.catalog.views.CatalogHtml'),
    url(r'^a/?$', 'apps.catalog.views.CatalogJson'),
    #url(r'^product/?$', 'apps.catalog.views.ProductHtml'),
    url(r'^a/product/?$', 'apps.catalog.views.ProductJson'),
    url(r'^a/product/category/?$', 'apps.catalog.views.ProductCategoryJson'),
    #url(r'^vendor/?$', 'apps.catalog.views.VendorHtml'),
    url(r'^a/vendor/?$', 'apps.catalog.views.VendorJson'),
)
