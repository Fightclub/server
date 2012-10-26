from django.db import models

class VendorCategory(models.Model):
  class Meta:
    app_label = "catalog"
  
  name   = models.CharField(max_length=128)
  icon   = models.URLField()

  def __unicode__(self):
    return self.name
