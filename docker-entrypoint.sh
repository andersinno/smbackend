#!/bin/bash

set -e
echo "Checking for database on host 'db', port 5432"
until nc -z -v -w30 "db" 5432
do
  echo "Waiting for postgres database connection..."
  sleep 1
done

export FIRST_RUN=$(./manage.py showmigrations 2>/dev/null | grep -q '^ .X.' && echo false || echo true)

# Apply database migrations
echo "Apply database migrations"
python /code/manage.py migrate --noinput

if $FIRST_RUN; then
python /code/manage.py geo_import finland --municipalities
python /code/manage.py turku_services_import services accessibility units addresses
fi

# Start server
echo "Starting server"
python /code/manage.py runserver 0.0.0.0:8000
