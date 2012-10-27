from django.db import models
from ProductCategory import ProductCategory

class Product(models.Model):
  class Meta:
    app_label = "catalog"
  
  name     = models.CharField(max_length=128)
  sku      = models.CharField(max_length=64)
  price    = models.DecimalField(max_digits=5, decimal_places=2)
  descr    = models.TextField()
  category = models.ManyToManyField(ProductCategory)
  icon     = models.URLField()
  vendor   = models.ForeignKey("Vendor")

  def to_dict(self, fields=None):
    productInfo = {}
    if not fields or "id" in fields:
      productInfo["id"] = self.id
    if not fields or "name" in fields:
      productInfo["name"] = self.name
    if not fields or "sku" in fields:
      productInfo["sku"] = self.sku
    if not fields or "price" in fields:
      productInfo["price"] = float(self.price)
    if not fields or "descr" in fields:
      productInfo["description"] = self.descr
    if not fields or "icon" in fields:
      productInfo["icon"] = self.icon
    if not fields or "vendor" in fields:
      productInfo["vendor"] = self.vendor.to_dict(["id", "name"])
    
    if not fields or "category" in fields:
      productInfo["categories"] = []
      for category in self.category.all():
        productInfo["categories"].append(category.to_dict(["id", "name"]))

    return productInfo

  def __unicode__(self):
    return self.sku
