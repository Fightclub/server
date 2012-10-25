from django.db import models
from VendorCategory import VendorCategory

class Vendor(models.Model):
  class Meta:
    app_label = "catalog"
  
  name     = models.CharField(max_length=128)
  descr    = models.TextField()
  category = models.ManyToManyField(VendorCategory)
  icon     = models.URLField()
  website  = models.URLField()
