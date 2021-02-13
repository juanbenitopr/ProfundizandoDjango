release: python manage.py migrate
web: gunicorn fetlix.wsgi:application -c gunicorn.conf.py -b 0.0.0.0:$PORT
