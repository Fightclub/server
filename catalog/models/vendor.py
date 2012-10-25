from django.db import models

class Vendor(models.Model):
  class Meta:
    app_label = "catalog"
  
  name    = models.CharField(max_length=128)
  descr   = models.TextField()
  icon    = models.URLField()
  website = models.URLField()
