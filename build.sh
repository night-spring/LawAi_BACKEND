#!/usr/bin/env bash

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input
