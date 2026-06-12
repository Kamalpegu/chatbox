#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate --noinput

# Collect static files (if you use them)
python manage.py collectstatic --noinput
