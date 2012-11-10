from django.test import Client, TestCase

from django.contrib.auth.models import User as DJUser
from apps.network.models import User
from apps.network.views import NewUserJson, UserLoginJson

class UserTest(TestCase):
  @classmethod
  def setUpClass(cls):
    cls.user1Data = {
        "email": "jsmith@example.com",
        "first": "John",
        "last": "Smith", 
        "password": "password", 
        "fbemail": "_john@facebook.com",
      }
    cls.user2Data = {
        "email": "zuck@example.net",
        "first": "Mark",
        "last": "Zuckerburg",
        "password": "password",
        "bday": "1984-05-14",
      }

    cls.user1 = User.create(cls.user1Data)
    cls.user2 = User.create(cls.user2Data)

  def setUp(self):
    self.c = Client()
    self.testUserData = {
        "email": "foo@bar.com",
        "first": "Foo",
        "last": "Bar",
        "password": "password",
        "bday": "2000-01-01",
      }
    self.testLoginCredentials = {
        "email": "jsmith@example.com",
        "fbemail": "_john@facebook.com",
        "password": "password",
      }

  def test_model_user_creates_djuser_email(self):
    djuser = DJUser.objects.get(email=UserTest.user2Data["email"])
    self.assertEqual(djuser.email, UserTest.user2Data["email"])

  def test_model_user_creates_djuser_firstname(self):
    djuser = DJUser.objects.get(email=UserTest.user1Data["email"])
    self.assertEqual(djuser.first_name, UserTest.user1Data["first"])

  def test_model_user_creates_djuser_lastname(self):
    self.assertEqual(UserTest.user1.user.last_name, UserTest.user1Data["last"])

  def test_model_user_stores_passwords_hashed(self):
    self.assertNotEqual(UserTest.user1.user.password, UserTest.user1Data["password"])

  def test_model_user_password_hashes_vary(self):
    self.assertNotEqual(UserTest.user1.user.password, UserTest.user2.user.password)

  def test_model_user_references_djuser(self):
    djuser = DJUser.objects.get(email=UserTest.user2Data["email"])
    self.assertEqual(djuser, UserTest.user2.user)

  def test_model_user_email_required(self):
    del self.testUserData["email"]
    with self.assertRaises(Exception):
      testUser = User.create(self.testUserData)

  def test_model_user_first_required(self):
    del self.testUserData["first"]
    with self.assertRaises(Exception):
      testUser = User.create(self.testUserData)

  def test_model_user_last_required(self):
    del self.testUserData["last"]
    with self.assertRaises(Exception):
      testUser = User.create(self.testUserData)

  def test_model_user_password_required(self):
    del self.testUserData["password"]
    with self.assertRaises(Exception):
      testUser = User.create(self.testUserData)

  def test_model_user_unique_email(self):
    self.testUserData["email"] = "jsmith@example.com"
    with self.assertRaises(Exception):
      testUser = User.create(self.testUserData)

  def test_model_user_unique_fbemail(self):
    self.testUserData["fbemail"] = "_john@facebook.com"
    with self.assertRaises(Exception):
      testUser = User.create(self.testUserData)

  def test_view_NewUserJson_missing_email(self):
    del self.testUserData["email"]
    response = self.c.get("/network/a/user/new", self.testUserData)
    self.assertEqual(response.content, "{\"error\": \"Required fields missing\"}")

  def test_view_NewUserJson_missing_first(self):
    del self.testUserData["first"]
    response = self.c.get("/network/a/user/new", self.testUserData)
    self.assertEqual(response.content, "{\"error\": \"Required fields missing\"}")

  def test_view_NewUserJson_missing_last(self):
    del self.testUserData["last"]
    response = self.c.get("/network/a/user/new", self.testUserData)
    self.assertEqual(response.content, "{\"error\": \"Required fields missing\"}")

  def test_view_NewUserJson_missing_password(self):
    del self.testUserData["password"]
    response = self.c.get("/network/a/user/new", self.testUserData)
    self.assertEqual(response.content, "{\"error\": \"Required fields missing\"}")

  def test_view_NewUserJson_existing_email(self):
    self.testUserData["email"] = "jsmith@example.com"
    response = self.c.get("/network/a/user/new", self.testUserData)
    self.assertEqual(response.content, "{\"error\": \"Email already used\"}")

  def test_view_NewUserJson_existing_fbemail(self):
    self.testUserData["fbemail"] = "_john@facebook.com"
    response = self.c.get("/network/a/user/new", self.testUserData)
    self.assertEqual(response.content, "{\"error\": \"Facebook account already associated\"}")

  def test_view_NewUserJson_Okay(self):
    response = self.c.get("/network/a/user/new", self.testUserData)
    self.assertEqual(", \"last\": \"Bar\", \"bday\": \"2000-01-01\", \"fbemail\": null, \"id\": 3, \"email\": \"foo@bar.com\", \"first\": \"Foo\"}" in response.content, True)

  def test_view_UserLoginJson_invalid_email(self):
    self.testLoginCredentials["email"] = "foo"
    response = self.c.get("/network/a/user/login", self.testLoginCredentials)
    self.assertEqual(response.content, "{\"error\": \"Invalid username/password\"}")
  
  def test_view_UserLoginJson_invalid_fbemail(self):
    del self.testLoginCredentials["email"]
    self.testLoginCredentials["fbemail"] = "foo"
    response = self.c.get("/network/a/user/login", self.testLoginCredentials)
    self.assertEqual(response.content, "{\"error\": \"Invalid username/password\"}")
  
  def test_view_UserLoginJson_invalid_fbemail(self):
    self.testLoginCredentials["password"] = "foo"
    response = self.c.get("/network/a/user/login", self.testLoginCredentials)
    self.assertEqual(response.content, "{\"error\": \"Invalid username/password\"}")
  
  def test_view_UserLoginJson_blank_emails(self):
    del self.testLoginCredentials["email"]
    del self.testLoginCredentials["fbemail"]
    response = self.c.get("/network/a/user/login", self.testLoginCredentials)
    self.assertEqual(response.content, "{\"error\": \"Invalid username/password\"}")

  def test_view_UserLoginJson_blank_password(self):
    del self.testLoginCredentials["password"]
    response = self.c.get("/network/a/user/login", self.testLoginCredentials)
    self.assertEqual(response.content, "{\"error\": \"Invalid username/password\"}")

  def test_view_UserLoginJson_Okay(self):
    response = self.c.get("/network/a/user/login", self.testLoginCredentials)
    self.assertEqual("apikey" in response.content, True)
