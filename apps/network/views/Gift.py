from django.http import HttpResponse
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder

from apps.catalog.models import Product
from apps.network.models import Gift
from apps.network.models import User

def NewGiftJson(request):
  data = request.GET
  giftInfo = {}
  apikey = data.get("apikey", None)
  product_id = data.get("product", None)
  receiver_id = data.get("receiver", None)
  receiver_email = data.get("email", None)

  if apikey and product_id and (receiver_id or receiver_email):
    sender = User.select(apikey=apikey)
    if sender:
      if receiver_id:
        recipient = User.select(id=receiver_id)
      if recipient and sender != recipient:
        try:
          product = Product.objects.get(id=product_id)
          gift = Gift(sender=sender, receiver=recipient, product=product)
          gift.save()
          giftInfo = gift.to_dict()
        except:
          giftInfo = {"error": "Invalid product"}
      else:
        giftInfo = {"error": "Invalid receiver"}
    else:
      giftInfo = {"error": "Invalid apikey"}
  
  return HttpResponse(json.dumps(giftInfo, cls=DjangoJSONEncoder))

