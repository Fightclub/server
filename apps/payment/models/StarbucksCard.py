from django.db import models

from Card import Card
from apps.catalog.models import Vendor

import mechanize, os

class StarbucksCard(Card):
  username = os.environ.get("FC_STARBUCKS_USERNAME")
  password = os.environ.get("FC_STARBUCKS_PASSWORD")

  cardManagerURL = "https://www.starbucks.com/account/card"
  browser = mechanize.Browser()

  @staticmethod
  def StarbucksLogin():
    response = StarbucksCard.browser.open(StarbucksCard.cardManagerURL)
    if response.geturl() != StarbucksCard.cardManagerURL:
      StarbucksCard.browser.select_form(nr=0)
      StarbucksCard.browser["Account.UserName"] = StarbucksCard.username
      StarbucksCard.browser["Account.PassWord"] = StarbucksCard.password
      response2 = StarbucksCard.browser.submit()
      if response2.geturl() == StarbucksCard.cardManagerURL:
        return True
      else:
        # Raise an exception?
        return False
    else:
      return True

  def RetrieveBalance(self):
    if StarbucksLogin():
      cardManagerResponse = self.browser.open(self.cardManagerURL)
      

  def __unicode__(self):
    return "%s: %s" % (self.vendor.name, self.cardID)
