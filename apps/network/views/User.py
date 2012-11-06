from django.http import HttpResponse
from django.utils import simplejson as json

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
    if not User.objects.filter(email=email):
      if not fbemail or not User.objects.filter(fbemail):
        try:
          newUser = User(first=first, last=last, bday=bday, email=email, fbemail=fbemail, password=password)
          newUser.save()
          userInfo = newUser.to_dict()
        except:
          userInfo = {}
      else:
        userInfo = {"error": "Facebook account already associated"}
    else:
      userInfo = {"error": "Email already used"}
  return HttpResponse(json.dumps(userInfo))

