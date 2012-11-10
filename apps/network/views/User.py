from django.http import HttpResponse
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.models import User as DJUser
from apps.network.models import User

def NewUserJson(request):
  data = request.GET
  userInfo = {}
  email = data.get("email", None)
  fbemail = data.get("fbemail", None)
  first = data.get("first", None)
  last = data.get("last", None)
  bday = data.get("bday", None)
  password = data.get("password", None)

  if email and first and last and password:
    if not DJUser.objects.filter(email=email):
      if not fbemail or not User.objects.filter(fbemail=fbemail):
        try:
          newDJUser = DJUser(first_name=first, last_name=last, email=email, password=password)
          newDJUser.save()
          newUser = User.objects.get(user=newDJUser)
          newUser.bday = bday
          newUser.fbemail = fbemail
          newUser.save()
          userInfo = newUser.to_dict()
        except:
          userInfo = {}
      else:
        userInfo = {"error": "Facebook account already associated"}
    else:
      userInfo = {"error": "Email already used"}
  return HttpResponse(json.dumps(userInfo, cls=DjangoJSONEncoder))

