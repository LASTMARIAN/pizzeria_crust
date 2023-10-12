#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r pizzeria/requirements.txtrequirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
