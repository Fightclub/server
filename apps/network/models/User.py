from django.db import models
from django.contrib.auth.models import User as DJUser
from django.db.models.signals import post_save

class User(models.Model):
  class Meta:
    app_label = "network"

  user     = models.OneToOneField(DJUser)
  bday     = models.DateField(blank=True, null=True)
  fbemail  = models.EmailField(unique=True, null=True, blank=True)

  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      profile, created = User.objects.get_or_create(user=instance)

  post_save.connect(create_user_profile, sender=DJUser)

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
    
    return userInfo

  def __unicode__(self):
    return "%s %s <%s>" % (self.user.first_name, self.user.last_name, self.user.email)

