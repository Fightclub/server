from django.http import HttpResponse
from django.utils import simplejson as json

from apps.catalog.models import Product, Vendor, VendorCategory

def VendorJson(request):
  data = request.GET
  vendorInfo = {}
  if data.get("id", None):
    try:
      vendorInfo = Vendor.objects.get(id=data.get("id")).to_dict()
    except:
      vendorInfo = {}
  return HttpResponse(json.dumps(vendorInfo))

def VendorHtml(request):
  return HttpResponse("Vendor Html")
