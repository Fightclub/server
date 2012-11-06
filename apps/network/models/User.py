from django.db import models

class User(models.Model):
  class Meta:
    app_label = "network"
  
  first    = models.CharField(max_length=64)
  last     = models.CharField(max_length=64)
  bday     = models.DateField(blank=True, null=True)
  email    = models.EmailField(unique=True)
  fbemail  = models.EmailField(unique=True, null=True)
  password = models.CharField(max_length=64)

  def to_dict(self, fields=None):
    userInfo = {}
    if not fields or "id" in fields:
      userInfo["id"] = self.id
    if not fields or "first" in fields:
      userInfo["first"] = self.first
    if not fields or "last" in fields:
      userInfo["last"] = self.last
    if not fields or "bday" in fields:
      userInfo["bday"] = self.bday
    if not fields or "email" in fields:
      userInfo["email"] = self.email
    if not fields or "fbemail" in fields:
      userInfo["fbemail"] = self.fbemail
    
    return userInfo

  def __unicode__(self):
    return "%s %s <%s>" % (self.first, self.last, self.fbemail)
