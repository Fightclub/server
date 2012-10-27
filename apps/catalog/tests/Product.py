from django.test import Client, TestCase

from apps.catalog.models import Product, ProductCategory, Vendor
from apps.catalog.views import ProductJson

class ProductTest(TestCase):
  def setUp(self):
    self.testCategory = ProductCategory(name="Test Category", icon="category icon path")
    self.testVendor = Vendor(name="Test Vendor", icon="test vendor icon")
    self.testVendor.save()
    self.testProduct = Product(name="Test Product", sku="testproduct", price="100.00", descr="This is a test product", icon="product icon", vendor=self.testVendor)
    self.testCategory.save()
    self.testProduct.save()
    self.testProduct.category.add(self.testCategory)
    self.c = Client()

  def test_model_product_not_none(self):
    self.assertNotEqual(self.testProduct, None)

  def test_model_product_has_id(self):
    self.assertEqual(self.testProduct.id, 1)

  def test_model_product_saved_name(self):
    self.assertEqual(self.testProduct.name, "Test Product")

  def test_model_product_saved_sku(self):
    self.assertEqual(self.testProduct.sku, "testproduct")

  def test_model_product_saved_price(self):
    self.assertEqual(self.testProduct.price, "100.00")

  def test_model_product_saved_descr(self):
    self.assertEqual(self.testProduct.descr, "This is a test product")

  def test_model_product_saved_vendor(self):
    self.assertEqual(self.testProduct.vendor.name, "Test Vendor")

  def test_model_product_saved_category(self):
    self.assertEqual(self.testProduct.category.all()[0].name, "Test Category")

  def test_view_undefined_product_json(self):
    response = self.c.get('/catalog/a/product', {'id': 0})
    self.assertEqual(response.content, "{}")

  def test_view_product_json(self):
    response = self.c.get('/catalog/a/product', {'id': 1})
    self.assertEqual(response.content, "{\"sku\": \"testproduct\", \"vendor\": {\"id\": 1, \"name\": \"Test Vendor\"}, \"description\": \"This is a test product\", \"price\": 100.0, \"name\": \"Test Product\", \"id\": 1, \"categories\": [{\"id\": 1, \"name\": \"Test Category\"}], \"icon\": \"product icon\"}")
