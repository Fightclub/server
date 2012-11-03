from django.test import Client, TestCase

from apps.payment.models import StarbucksCard
from apps.catalog.models import Vendor

class StarbucksCardTest(TestCase):
  def setUp(self):
    self.testVendor = Vendor(name="Starbucks", icon="https://www.starbucks.com/static/images/global/logo.png")
    self.testVendor.save()
    self.testCard = StarbucksCard(name="TestCard", cardID="8C6272FB99D71A", value=0.0, vendor=self.testVendor)
    self.testCard.save()

  def test_model_card_not_none(self):
    self.assertNotEqual(self.testCard, None)

  def test_model_starbucks_login(self):
    self.assertEqual(StarbucksCard.StarbucksLogin(), True)

