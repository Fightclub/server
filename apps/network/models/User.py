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
  def select(cls, email=None, fbemail=None, id=None):
    user = None
    if id:
      try:
        user = cls.objects.get(id=id)
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
        user = User.objects.get(fbemail=fbemail)
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

