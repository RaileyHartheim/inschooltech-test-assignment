#!/bin/sh


until cd /app/backend/
do
    echo 'Waiting for Django...'
done

until python manage.py migrate
do
    echo "Waiting for PostgreSQL..."
    sleep 1
done

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn backend.wsgi --bind 0.0.0.0:8000