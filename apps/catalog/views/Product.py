from django.http import HttpResponse
from django.utils import simplejson as json

from apps.catalog.models import Product, ProductCategory, Vendor

def ProductJson(request):
  data = request.GET
  productInfo = {}
  if data.get("id", None):
    try:
      product = Product.objects.get(id=data.get("id", None))
    except:
      product = None

    if product:
      productInfo["name"] = product.name
      productInfo["sku"] = product.sku
      productInfo["price"] = float(product.price)
      productInfo["description"] = product.descr
      productInfo["icon"] = product.icon
      productInfo["vendorid"] = product.vendor.id

      productInfo["categories"] = []
      for category in product.category.all():
        productInfo["categories"].append(category.id)

  return HttpResponse(json.dumps(productInfo))

def ProductHtml(request):
  return HttpResponse("Product Html")

