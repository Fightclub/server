import os

import redis
from rq import Worker, Queue, Connection

listen = ["high", "default", "low"]

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == "__main__":
  fc_env = os.environ.get("FC_ENV")
  if fc_env == None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
  else:
    if fc_env.lower() == "dev":
      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
    elif fc_env.lower() == "heroku-beta":
      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.heroku-beta")
    elif fc_env.lower() == "heroku-production":
      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.heroku-production")
    else:
      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
  with Connection(conn):
    worker = Worker(map(Queue, listen))
    worker.work()
