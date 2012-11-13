import os
from urlparse import urlparse

redisurl = urlparse(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
if redisurl.hostname == "localhost":
  rqscheduler = "/usr/local/lib/python2.7/site-packages/rq_scheduler/scripts/rqscheduler.py"
else:
  rqscheduler = "/app/.heroku/venv/lib/python2.7/site-packages/rq_scheduler/scripts/rqscheduler.py"
command = "python %s -H %s -p %s" % (rqscheduler, redisurl.hostname, redisurl.port)

if redisurl.password:
  command += " -P " + redisurl.password
os.system(command + " &")
