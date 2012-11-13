web: `python ./manage.py runserver 0.0.0.0:$PORT --noreload`
worker: `python manage.py rqworker high default low`
scheduler: `python /app/.heroku/venv/lib/python2.7/site-packages/rq_scheduler/scripts/rqscheduler.py`
all: `python start_all.py`
