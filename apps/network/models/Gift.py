from django.db import models

from apps.catalog.models import Product
from apps.network.models import User

class Gift(models.Model):
  class Meta:
    app_label = "network"

  sender   = models.ForeignKey(User, related_name="sent")
  receiver = models.ForeignKey(User, related_name="received")
  product  = models.ForeignKey(Product)
  created  = models.DateTimeField(auto_now=True)
  redeemed = models.DateTimeField(null=True, blank=True)

  def to_dict(self, fields=None):
    giftInfo = {}
    if not fields or "sender" in fields:
      giftInfo["sender"] = self.sender.to_dict(fields=["first", "last", "id"])
    if not fields or "receiver" in fields:
      giftInfo["receiver"] = self.receiver.to_dict(fields=["first", "last", "id"])
    if not fields or "product" in fields:
      giftInfo["product"] = self.product.to_dict(fields=["name", "icon", "vendor"])
    if not fields or "created" in fields:
      giftInfo["created"] = self.created
    if not fields or "redeemed" in fields:
      giftInfo["redeemed"] = self.redeemed
    
    return giftInfo

  def __unicode__(self):
    return "%s %s -> %s" % (self.product.name, self.sender.user.email, self.receiver.user.email)

