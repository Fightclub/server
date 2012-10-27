from django.db import models
from VendorCategory import VendorCategory

class Vendor(models.Model):
  class Meta:
    app_label = "catalog"
  
  name       = models.CharField(max_length=128)
  descr      = models.TextField()
  category   = models.ManyToManyField(VendorCategory)
  icon       = models.URLField()
  website    = models.URLField()

  def to_dict(self, fields=None):
    vendorInfo = {}
    if not fields or "id" in fields:
      vendorInfo["id"] = self.id
    if not fields or "name" in fields:
      vendorInfo["name"] = self.name
    if not fields or "descr" in fields:
      vendorInfo["description"] = self.descr
    if not fields or "icon" in fields:
      vendorInfo["icon"] = self.icon
    if not fields or "website" in fields:
      vendorInfo["website"] = self.website
    return vendorInfo

  def __unicode__(self):
    return self.name
