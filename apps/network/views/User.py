from django.http import HttpResponse
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder

from django.contrib.auth.models import User as DJUser
from apps.network.models import User

def NewUserJson(request):
  data = request.GET
  userInfo = {}
  userData = {                          
      "email": data.get("email", None), 
      "first": data.get("first", None), 
      "last": data.get("last", None),
      "password": data.get("password", None),
      "fbemail": data.get("fbemail", None),
      "bday": data.get("bday", None),
    }

  try:
    newUser = User.create(userData)
    userInfo = newUser.to_dict()
  except Exception, err:
    userInfo = {"error": str(err)}
  return HttpResponse(json.dumps(userInfo, cls=DjangoJSONEncoder))

def UserLoginJson(request):
  data = request.GET
  email = data.get("email", None)
  fbemail = data.get("fbemail", None)
  password = data.get("password", None)
  response = {"error": "Invalid username/password"}

  if password and (email or fbemail):
    if email:
      user = User.select(email=email)
    else:
      user = User.select(fbemail=fbemail)
    if user and user.user.check_password(password):
      response = user.to_dict()
  return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder))
