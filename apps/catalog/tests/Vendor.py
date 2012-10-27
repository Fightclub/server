from django.test import Client, TestCase

from apps.catalog.models import Product, ProductCategory, Vendor, VendorCategory
from apps.catalog.views import VendorJson

class VendorTest(TestCase):
  def setUp(self):
    self.testCategory = VendorCategory(name="Test Category", icon="category icon path")
    self.testVendor = Vendor(name="Test Vendor", icon="test vendor icon", descr="Test vendor description", website="test vendor website")
    self.testVendor.save()
    self.testProduct = Product(name="Test Product", sku="testproduct", price="100.00", descr="This is a test product", icon="product icon", vendor=self.testVendor)
    self.testCategory.save()
    self.testProduct.save()
    self.testVendor.category.add(self.testCategory)
    self.c = Client()

  def test_model_vendor_not_none(self):
    self.assertNotEqual(self.testVendor, None)

  def test_model_vendor_has_id(self):
    self.assertEqual(self.testVendor.id, 1)

  def test_model_vendor_saved_name(self):
    self.assertEqual(self.testVendor.name, "Test Vendor")

  def test_model_vendor_saved_descr(self):
    self.assertEqual(self.testVendor.descr, "Test vendor description")

  def test_model_vendor_saved_website(self):
    self.assertEqual(self.testVendor.website, "test vendor website")

  def test_model_vendor_saved_category(self):
    self.assertEqual(self.testVendor.category.all()[0].name, "Test Category")

  def test_model_vendor_product_list(self):
    self.assertEqual(self.testVendor.product_set.all()[0].name, "Test Product")

  def test_view_undefined_vendor_json(self):
    response = self.c.get('/catalog/a/vendor', {'id': 0})
    self.assertEqual(response.content, "{}")

  def test_view_vendor_json(self):
    response = self.c.get('/catalog/a/vendor', {'id': 1})
    self.assertEqual(response.content, "{\"website\": \"test vendor website\", \"description\": \"Test vendor description\", \"icon\": \"test vendor icon\", \"id\": 1, \"name\": \"Test Vendor\"}")
