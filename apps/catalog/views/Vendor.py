from django.http import HttpResponse
from django.utils import simplejson as json

from apps.catalog.models import Product, Vendor, VendorCategory

def VendorJson(request):
  data = request.GET
  vendorInfo = {}
  if data.get("id", None):
    try:
      vendor = Vendor.objects.get(id=data.get("id", None))
    except:
      vendor = None

    if vendor:
      vendorInfo["name"] = vendor.name
      vendorInfo["description"] = vendor.descr
      vendorInfo["icon"] = vendor.icon
      vendorInfo["website"] = vendor.website

      vendorInfo["categories"] = []
      for category in vendor.category.all():
        vendorInfo["categories"].append(category.id)

  return HttpResponse(json.dumps(vendorInfo))

def VendorHtml(request):
  return HttpResponse("Vendor Html")
