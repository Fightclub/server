from django.db import models

from apps.catalog.models import Product
from apps.network.models import User
from apps.payment.models import Card

from datetime import datetime, timedelta
from django.utils.timezone import utc

import django_rq as rq

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
  payment  = models.ForeignKey(Card.Card, null=True, blank=True)

  def Redeem(self):
    if self.status == Gift.GIFT_STATUS_CREATED:
      try:
        card = Card.Card.objects.filter(vendor=self.product.vendor, user=None, master=False)[:1]
      except Card.Card.DoesNotExist:
        card = None
      expireTimeUTC = None
      if card:
        card = card[0]
        card.user = self.receiver
        card.save()
        queue = rq.get_queue('high')
        load = queue.enqueue(Card.SetBalance, card.id, self.product.price)
        scheduler = rq.get_scheduler('low')
        expireTimeUTC = datetime.utcnow() + timedelta(minutes=5)
        expireTime = datetime.now() + timedelta(minutes=5)
        unload = scheduler.enqueue_at(expireTime, CheckRedemption, self.id)
        self.activated = datetime.utcnow().replace(tzinfo=utc)
        self.status = self.GIFT_STATUS_ACTIVE
        self.payment = card
        self.save()
    elif self.status == Gift.GIFT_STATUS_ACTIVE:
      card = self.payment
      expireTimeUTC = self.activated + timedelta(minutes=5)
    return (card, expireTimeUTC)

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

def CheckRedemption(giftID):
  gift = Gift.objects.get(id=giftID)
  card = gift.payment.ProxyCard()
  databaseBalance = card.value
  if databaseBalance == card.RetrieveBalance():
    # No change to card value, user did not buy anything
    gift.status = Gift.GIFT_STATUS_CREATED
    gift.payment = None
    gift.activated = None
  else:
    # Payment was used to buy something
    gift.status = Gift.GIFT_STATUS_REDEEMED
    gift.payment = None
    gift.redeemed = datetime.utcnow().replace(tzinfo=utc)
  card.user = None
  card.save()
  card.SetBalance(0)
  gift.save()
  masterCard = Card.Card.objects.filter(vendor=gift.product.vendor, master=True)[:1]
  if masterCard:
    masterCard = masterCard[0].ProxyCard()
    masterCard.value = masterCard.RetrieveBalance()
    masterCard.save()

