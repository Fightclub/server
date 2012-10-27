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

  def __unicode__(self):
    return self.sku
