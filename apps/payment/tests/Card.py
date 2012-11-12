from django.test import Client, TestCase

import apps.payment.models.Card as Card
from apps.catalog.models import Vendor

class CardTest(TestCase):
  @classmethod
  def setUpClass(cls):
    cls.testVendor = Vendor(name="Starbucks", icon="https://www.starbucks.com/static/images/global/logo.png")
    cls.testVendor.save()
    cls.testCard = Card.Card(name="TestCard", cardID="8C6272FB99D71A", value=0.0, vendor=cls.testVendor)
    cls.testCard.save()

  @classmethod
  def tearDownClass(cls):
    Card.SetBalance(CardTest.testCard.id, 0.0)

  def test_model_card_RetrieveValue(self):
    self.assertEqual(Card.RetrieveBalance(CardTest.testCard.id), 0.0)

  def test_model_card_SetBalance(self):
    Card.SetBalance(CardTest.testCard.id, 1.0)
    CardTest.testCard = Card.Card.objects.get(id=CardTest.testCard.id)
    self.assertEqual(CardTest.testCard.value, 1.0)
