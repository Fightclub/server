from django.http import HttpResponse
from django.utils import simplejson as json

from apps.catalog.models import Product, ProductCategory, Vendor

def ProductCategoryJson(request):
  data = request.GET
  productCategoryInfo = {}
  if data.get("id", None):
    try:
      productCategory = ProductCategory.objects.get(id=data.get("id", None))
    except:
      productCategory = None

    if productCategory:
      productCategoryInfo["name"] = productCategory.name
      productCategoryInfo["icon"] = productCategory.icon

      productCategoryInfo["products"] = []
      for product in productCategory.product_set.all():
        productCategoryInfo["products"].append(product.id)

  return HttpResponse(json.dumps(productCategoryInfo))

def ProductCategoryHtml(request):
  return HttpResponse("Product Category Html")

