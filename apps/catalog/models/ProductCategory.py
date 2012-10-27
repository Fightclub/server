from django.db import models

class ProductCategory(models.Model):
  class Meta:
    app_label = "catalog"
  
  name   = models.CharField(max_length=128)
  icon   = models.URLField()

  def to_dict(self, fields=None):
    productCategoryInfo = {}
    if not fields or "id" in fields:
      productCategoryInfo["id"] = self.id
    if not fields or "name" in fields:
      productCategoryInfo["name"] = self.name
    if not fields or "icon" in fields:
      productCategoryInfo["icon"] = self.icon

    return productCategoryInfo

  def __unicode__(self):
    return self.name
