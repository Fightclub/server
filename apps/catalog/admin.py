from django.contrib import admin
from apps.catalog.models import *

admin.site.register([Product, ProductCategory, Vendor, VendorCategory])
