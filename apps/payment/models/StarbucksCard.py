from django.db import models

from Card import Card
from apps.catalog.models import Vendor

import mechanize, os
from bs4 import BeautifulSoup

class StarbucksCard(Card):
  username = os.environ.get("FC_STARBUCKS_USERNAME")
  password = os.environ.get("FC_STARBUCKS_PASSWORD")

  cardManagerURL = "https://www.starbucks.com/account/card"
  browser = mechanize.Browser()

  @staticmethod
  def StarbucksLogin():
    if not StarbucksCard.username and not StarbucksCard.password:
      raise Exception("FC_STARBUCKS_USERNAME or FC_STARBUCKS_PASSWORD not set") 
    try:
      response = StarbucksCard.browser.open(StarbucksCard.cardManagerURL)
    except:
      raise Exception("Could connect to Starbucks server")
    if response.geturl() != StarbucksCard.cardManagerURL:
      StarbucksCard.browser.select_form(nr=0)
      StarbucksCard.browser["Account.UserName"] = StarbucksCard.username
      StarbucksCard.browser["Account.PassWord"] = StarbucksCard.password
      response2 = StarbucksCard.browser.submit()
      if response2.geturl() == StarbucksCard.cardManagerURL:
        return True
      else:
        raise Exception("Starbucks login failed")
    else:
      return True

  @staticmethod
  def StarbucksBalance(cardID):
    try:
      StarbucksCard.StarbucksLogin()
      cardManagerResponse = StarbucksCard.browser.open(StarbucksCard.cardManagerURL)
      StarbucksCard.browser.select_form(nr=0)
      selectedCardResponse = StarbucksCard.browser.submit(cardID)
      parser = BeautifulSoup(selectedCardResponse.read())
      balanceSpan = parser.findAll('span', attrs={'class':'balance numbers'})
      return float(str(balanceSpan[0].findAll(text=True)[0])[1:])
    except:
      return -1.0

  def RetrieveBalance(self):
    return StarbucksCard.StarbucksBalance(self.cardID)

  def __unicode__(self):
    return "%s: %s" % (self.vendor.name, self.cardID)
