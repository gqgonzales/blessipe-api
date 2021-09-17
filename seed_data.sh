#!/bin/bash

rm -rf blessipeapi/migrations
rm db.sqlite3
python manage.py makemigrations blessipeapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata countries
python manage.py loaddata cities
python manage.py loaddata travelers
python manage.py loaddata restaurants
python manage.py loaddata recipes
python manage.py loaddata keywords
python manage.py loaddata recipe_keywords
python manage.py loaddata restaurant_keywords



