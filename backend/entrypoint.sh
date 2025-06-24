#!/bin/bash

set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

while ! nc -z redis 6379; do
  sleep 1
done

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn chemistry_shop.wsgi:application --bind 0.0.0.0:8000 --workers 2

stripe listen --forward-to localhost:8000/payment/webhook-stripe/

exec "$@"