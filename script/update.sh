#!/usr/bin/env bash
cd ..
git fetch --all
git pull
python manage.py makemigrations
python manage.py migrate
bash restart_server.sh