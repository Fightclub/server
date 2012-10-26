from django.http import HttpResponse
from django.utils import simplejson as json

def CatalogJson(request):
  return HttpResponse("Catalog Json")

def CatalogHtml(request):
  return HttpResponse("Catalog Html")
