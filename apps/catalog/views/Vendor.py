from django.http import HttpResponse
from django.utils import simplejson as json

def VendorJson(request):
  return HttpResponse("Vendor Json")

def VendorHtml(request):
  return HttpResponse("Vendor Html")
