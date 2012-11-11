import random, sha

from django.db import models
from django.contrib.auth.models import User as DJUser
from django.db.models.signals import post_save

class User(models.Model):
  class Meta:
    app_label = "network"

  user     = models.OneToOneField(DJUser)
  bday     = models.DateField(blank=True, null=True)
  fbemail  = models.EmailField(unique=True, null=True, blank=True)
  apikey   = models.CharField(max_length=40)

  @classmethod
  def create(cls, data):
    if "email" in data and data["email"] and \
       "first" in data and data["first"] and \
       "last" in data and data["last"] and \
       "password" in data and data["password"]:
      if not DJUser.objects.filter(email=data["email"]):
        if not ("fbemail" in data and data["fbemail"]) or not User.objects.filter(fbemail=data["fbemail"]):
          newDJUser = DJUser(username=data["email"], first_name=data["first"], last_name=data["last"], email=data["email"])
          newDJUser.set_password(data["password"])
          newDJUser.save()
          newUser = User.objects.get(user=newDJUser)
          newUser.bday = data["bday"] if "bday" in data and data["bday"] else None
          newUser.fbemail = data["fbemail"] if "fbemail" in data and data["fbemail"] else None
          newUser.apikey = newUser.generate_apikey()
          newUser.save()
        else:
          raise Exception("Facebook account already associated")
      else:
        raise Exception("Email already used")
    else:
      raise Exception("Required fields missing")
    return newUser

  @classmethod
  def select(cls, email=None, fbemail=None, id=None, apikey=None):
    user = None
    if id:
      try:
        user = cls.objects.get(id=id)
      except:
        pass
    elif apikey:
      try:
        user = cls.objects.get(apikey=apikey)
      except:
        pass
    elif email:
      try:
        djuser = DJUser.objects.get(email=email)
        user = cls.objects.get(user=djuser)
      except:
        pass
    elif fbemail:
      try:
        user = cls.objects.get(fbemail=fbemail)
      except:
        pass
    return user

  def generate_apikey(self):
    salt = sha.new(str(random.random())).hexdigest()[:5]
    return sha.new(salt+self.user.email).hexdigest()

  def create_djuser(sender, instance, created, **kwargs):
    if created:
      profile, created = User.objects.get_or_create(user=instance)

  post_save.connect(create_djuser, sender=DJUser)

  def to_dict(self, fields=None):
    userInfo = {}
    if not fields or "id" in fields:
      userInfo["id"] = self.id
    if not fields or "first" in fields:
      userInfo["first"] = self.user.first_name
    if not fields or "last" in fields:
      userInfo["last"] = self.user.last_name
    if not fields or "bday" in fields:
      userInfo["bday"] = self.bday
    if not fields or "email" in fields:
      userInfo["email"] = self.user.email
    if not fields or "fbemail" in fields:
      userInfo["fbemail"] = self.fbemail
    if not fields or "apikey" in fields:
      userInfo["apikey"] = self.apikey
    
    return userInfo

  def __unicode__(self):
    return "%s %s <%s>" % (self.user.first_name, self.user.last_name, self.user.email)

