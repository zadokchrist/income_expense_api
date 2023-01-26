web: gunicorn incomeexpenseapi.wsgi
release: python manage.py makemigrations --noinput
release: python manage.py collectstatic 1 --noinput
release: python manage.py migrate --noinput