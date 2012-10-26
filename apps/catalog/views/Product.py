from django.http import HttpResponse
from django.utils import simplejson as json

def ProductJson(request):
  return HttpResponse("Product Json")

def ProductHtml(request):
  return HttpResponse("Product Html")
