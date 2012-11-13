import os
from urlparse import urlparse

os.system("python ./manage.py runserver 0.0.0.0:$PORT --noreload &")
os.system("python manage.py rqworker high default low &")
os.system("python scheduler.py &")
