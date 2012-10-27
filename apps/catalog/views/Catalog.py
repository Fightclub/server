from django.http import HttpResponse
from django.utils import simplejson as json

from apps.catalog.models import ProductCategory, Vendor

def CatalogJson(request):
  data = request.GET
  catalogInfo = {}

  catalogInfo["categories"] = []
  for category in ProductCategory.objects.all():
    catalogInfo["categories"].append(category.to_dict(["id", "name", "icon"]))

  catalogInfo["vendors"] = []
  for vendor in Vendor.objects.all():
    catalogInfo["vendors"].append(vendor.to_dict(fields=["id", "name", "icon"]))

  return HttpResponse(json.dumps(catalogInfo))

def CatalogHtml(request):
  return HttpResponse("Catalog Html")
