from django.db import models

from Card import Card
from apps.catalog.models import Vendor

import mechanize, os
from bs4 import BeautifulSoup

class StarbucksCard(Card):
  class Meta:
    proxy = True

  username = os.environ.get("FC_STARBUCKS_USERNAME")
  password = os.environ.get("FC_STARBUCKS_PASSWORD")

  cardManagerURL = "https://www.starbucks.com/account/card"
  transferFundsURL = "https://www.starbucks.com/account/card/transfer"
  browser = mechanize.Browser(
      factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True)
      )

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
    StarbucksCard.StarbucksLogin()
    cardManagerResponse = StarbucksCard.browser.open(StarbucksCard.cardManagerURL)
    StarbucksCard.browser.select_form(nr=0)
    selectedCardResponse = StarbucksCard.browser.submit(cardID)
    parser = BeautifulSoup(selectedCardResponse.read())
    balanceSpan = parser.findAll('span', attrs={'class':'balance numbers'})
    return float(str(balanceSpan[0].findAll(text=True)[0])[1:])

  @staticmethod
  def TransferFunds(fromCard, toCard, amount):
    StarbucksCard.StarbucksLogin()
    fromAmount = StarbucksCard.StarbucksBalance(fromCard)
    if amount > fromAmount:
      raise Exception("Card does not have sufficient funds")
    else:
      transferOriginResponse = StarbucksCard.browser.open(StarbucksCard.transferFundsURL)
      StarbucksCard.browser.select_form(nr=0)
      selectedCardResponse = StarbucksCard.browser.submit(fromCard)
      transferOriginResponse = StarbucksCard.browser.open(StarbucksCard.transferFundsURL)
      StarbucksCard.browser.select_form(nr=1)
      transferFromResponse = StarbucksCard.browser.submit(name="TransferFrom")
      StarbucksCard.browser.select_form(nr=1)
      StarbucksCard.browser["TransferFrom.ExistingCardId"] = [toCard]
      transferToResponse = StarbucksCard.browser.submit()
      StarbucksCard.browser.select_form(nr=1)
      StarbucksCard.browser["TransferFrom.TransferAmount"] = str(amount)
      previewResponse = StarbucksCard.browser.submit()
      StarbucksCard.browser.select_form(nr=1)
      transferResponse = StarbucksCard.browser.submit()

  def RetrieveBalance(self):
    return StarbucksCard.StarbucksBalance(self.cardID)

  def SetBalance(self, balance):
    currentBalance = self.RetrieveBalance()
    masterCard = StarbucksCard.objects.get(master=True)
    masterValue = float(masterCard.value)
    if currentBalance < balance:
      masterCard.value = masterValue - (balance-currentBalance)
      self.value = balance
      masterCard.save()
      self.save()
      StarbucksCard.TransferFunds(masterCard.cardID, self.cardID, balance-currentBalance)
    elif currentBalance > balance:
      masterCard.value = masterValue + (currentBalance-balance)
      self.value = balance
      masterCard.save()
      self.save()
      StarbucksCard.TransferFunds(self.cardID, masterCard.cardID, currentBalance-balance)

