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

  def test_model_productCategory_not_none(self):
    self.assertNotEqual(self.testCategory, None)

  def test_model_productCategory_has_id(self):
    self.assertEqual(self.testCategory.id, 1)

  def test_model_productCategory_saved_name(self):
    self.assertEqual(self.testCategory.name, "Test Category")

  def test_model_productCategory_saved_icon(self):
    self.assertEqual(self.testCategory.icon,"category icon path")

  def test_model_productCategory_product_list(self):
    self.assertEqual(self.testCategory.product_set.all()[0].name, "Test Product")

  def test_view_undefined_productCategory_json(self):
    response = self.c.get('/catalog/a/product/category', {'id': 0})
    self.assertEqual(response.content, "{}")

  def test_view_productCategory_json(self):
    response = self.c.get('/catalog/a/product/category', {'id': 1})
    self.assertEqual(response.content, "{\"icon\": \"category icon path\", \"products\": [{\"icon\": \"product icon\", \"vendor\": {\"icon\": \"test vendor icon\", \"id\": 1, \"name\": \"Test Vendor\"}, \"id\": 1, \"name\": \"Test Product\"}], \"id\": 1, \"name\": \"Test Category\"}")
