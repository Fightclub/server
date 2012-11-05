from django.db import models
from apps.catalog.models import Vendor

class Card(models.Model):
  class Meta:
    abstract = True
    app_label = "payment"
    db_table = "payment_cards"
  
  name     = models.CharField(max_length=128)
  cardID   = models.CharField(max_length=64)
  value    = models.DecimalField(max_digits=5, decimal_places=2)
  vendor   = models.ForeignKey(Vendor)
  # TODO: once we have a notion of "users" we should add a user mapping here

  def RetrieveBalance(self):
    raise NotImplementedError("RetrieveBalance not implemented")

  def SetBalance(self, value):
    raise NotImplementedError("SetBalance not implemented")

  def __unicode__(self):
    raise NotImplementedError("__unicode__ not implemented")
