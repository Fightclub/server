from django.db import models

from apps.catalog.models import Vendor
from apps.network.models import User

class Card(models.Model):
  class Meta:
    app_label = "payment"
    db_table = "payment_cards"
  
  name     = models.CharField(max_length=128)
  cardID   = models.CharField(max_length=64)
  value    = models.DecimalField(max_digits=5, decimal_places=2)
  vendor   = models.ForeignKey(Vendor)
  user     = models.ForeignKey(User, null=True, blank=True)
  master   = models.BooleanField(default=False)
  
  redemptionImage = models.URLField()
  barcodeImage    = models.URLField()


  def ProxyCard(self):    
    from StarbucksCard import StarbucksCard

    CARD_CLASSES = {
      "Starbucks": StarbucksCard
    }
    if self.vendor.name in CARD_CLASSES:
      return CARD_CLASSES[self.vendor.name].objects.get(id=self.id)
    else:
      return None

  def RetrieveBalance(self):
    raise NotImplementedError("RetrieveBalance not implemented")

  def SetBalance(self, value):
    raise NotImplementedError("SetBalance not implemented")

  def __unicode__(self):
    return "%s: %s" % (self.vendor.name, self.cardID)

def RetrieveBalance(cardID):
  proxy = Card.objects.get(id=cardID).ProxyCard()
  return proxy.RetrieveBalance()

def SetBalance(cardID, balance):
  proxy = Card.objects.get(id=cardID).ProxyCard()
  return proxy.SetBalance(float(balance))

