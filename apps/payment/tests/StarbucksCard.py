from django.test import Client, TestCase

from apps.payment.models import StarbucksCard
from apps.catalog.models import Vendor

class StarbucksCardTest(TestCase):
  @classmethod
  def setUpClass(cls):
    cls.testVendor = Vendor(name="Starbucks", icon="https://www.starbucks.com/static/images/global/logo.png")
    cls.testVendor.save()
    cls.testCard = StarbucksCard(name="TestCard", cardID="8C6272FB99D71A", value=0.0, vendor=cls.testVendor)
    cls.testCard.save()

  @classmethod
  def tearDownClass(cls):
    cls.testCard.SetBalance(0.0)

  def test_model_card_not_none(self):
    self.assertNotEqual(self.testCard, None)

  def test_model_starbucks_login(self):
    self.assertEqual(StarbucksCard.StarbucksLogin(), True)

  def test_model_starbucks_RetrieveValue(self):
    self.assertEqual(StarbucksCardTest.testCard.RetrieveBalance(), 0.0)

  def test_model_starbucks_SetBalance(self):
    StarbucksCardTest.testCard.SetBalance(1.0)
    self.assertEqual(StarbucksCardTest.testCard.value, 1.0)
