from django.http import HttpResponse
from django.utils import simplejson as json

from apps.catalog.models import Product, ProductCategory, Vendor

def ProductJson(request):
  data = request.GET
  productInfo = {}
  if data.get("id", None):
    try:
      productInfo = Product.objects.get(id=data.get("id", None)).to_dict()
    except:
      productInfo = {}
  return HttpResponse(json.dumps(productInfo))

def ProductHtml(request):
  return HttpResponse("Product Html")
