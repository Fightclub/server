from django.db import models

from apps.catalog.models import Product
from apps.network.models import User
from apps.payment.models import Card

from datetime import datetime
from django.utils.timezone import utc

class Gift(models.Model):
  class Meta:
    app_label = "network"

  # Gift statuses:
  GIFT_STATUS_CREATED = "C"
  GIFT_STATUS_ACTIVE = "A"
  GIFT_STATUS_REDEEMED = "R"

  GIFT_STATUS = (
    (GIFT_STATUS_CREATED, "Created"),
    (GIFT_STATUS_ACTIVE, "Active"),
    (GIFT_STATUS_REDEEMED, "Redeemed"),
  )

  sender   = models.ForeignKey(User, related_name="sent")
  receiver = models.ForeignKey(User, related_name="received")
  product  = models.ForeignKey(Product)
  status   = models.CharField(max_length=1, choices=GIFT_STATUS, default=GIFT_STATUS_CREATED)
  created  = models.DateTimeField(auto_now=True)
  activated = models.DateTimeField(null=True, blank=True)
  redeemed = models.DateTimeField(null=True, blank=True)

  def Redeem(self):
    card = Card.objects.filter(vendor=self.product.vendor, user=None)[:1]
    if card:
      self.activated = datetime.utcnow().replace(tzinfo=utc)
      self.status = self.GIFT_STATUS_ACTIVE
      self.save()

  def to_dict(self, fields=None):
    giftInfo = {}
    if not fields or "id" in fields:
      giftInfo["id"] = self.id
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

