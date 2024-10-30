#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput

python manage.py setup_roles_and_groups 

if [ "$APPLICATION_MODE" = "production" ]; then
    python manage.py collectstatic --noinput
    gunicorn base.wsgi:application --bind 0.0.0.0:5000 --workers 3
else
    
    python manage.py runserver 0.0.0.0:5000
    
fi

